from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django.db.models import Q,F
import django_excel as excel
import xlrd
import re
from django.db.models import Count,Sum,Value, When,Case,IntegerField,CharField
from django.urls import reverse_lazy
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings

from .models import Container
from .forms import ContainerForm
from  bayplan.models import BayPlanFile



under_deck = ['16','14','12','10','08','06','04','02']
over_deck =['90','88','86','84','82','80']

tier1 =['10','08','06','04','02','00','01','03','05','07','09']
tier2 =['12','10','08','06','04','02','00','01','03','05','07','09','11']



class ContainerDetailView(LoginRequiredMixin,DetailView):
	model = Container
	# def get_queryset(self):
	# 	slug = self.kwargs['slug']
	# 	return Container.objects.filter(slug=slug)

class ContainerUpdateView(LoginRequiredMixin,UpdateView):
	model = Container
	template_name = 'container/container_detail_update.html'
	form_class = ContainerForm
	# success_url = reverse_lazy('container:detail',kwargs={})

	def get_queryset(self):
		qs = super(ContainerUpdateView, self).get_queryset()
		return qs.all()

	def get_form_kwargs(self):
		kwargs = super(ContainerUpdateView,self).get_form_kwargs()
		kwargs['stowage'] = self.object.stowage
		return kwargs

	def get_success_url(self,*args, **kwargs):
		# print('Slug %s' % self.object.bayplanfile.slug)
		mode = self.request.GET.get('mode')
		

		print(mode)
		slug =self.object.bayplanfile.slug
		bay = self.object.bay
		# print ('Bay %s'% bay)
		if mode=='search':
			query = self.request.GET.get('q')
			url = reverse('container:bay',kwargs={'slug':slug})
			url = '%s?q=%s' % (url , query)
		else :
			url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
			url = '%s?q=%s' % (url , self.object.container)
		
		return url
		# reverse_lazy('container:detail',kwargs={'slug':slug,'bay':bay},query={'q':self.object.container})
		# return reverse(url)

	def form_valid(self,form,*args, **kwargs):
		# action = request.GET.get('action')
		# print ('Valid form %s' % action)
		obj = form.save(commit=False)
		# obj.user = self.request.user
		return super(ContainerUpdateView,self).form_valid(form)


class ContainerListView(LoginRequiredMixin,ListView):
	# template_name = 'restaurants/restaurants_list.html' # default name =restaurantlocation_list.html
	model = Container
	# def get_queryset(self):
	# 	slug = self.kwargs['slug']
	# 	return Container.objects.filter(bayplanfile__slug = slug)

def ContainerRestore(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	c = Container.objects.get(slug=slug)
	c.stowage = c.original_stowage
	c.bay = c.original_bay
	c.save()


	slug = c.bayplanfile.slug
	bay = c.bay

	mode = request.GET.get('mode')
	if mode=='search':
		query = request.GET.get('q')
		url = reverse('container:bay',kwargs={'slug':slug})
		url = '%s?q=%s' % (url , query)
	else:
		url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
		url = '%s?q=%s' % (url , c.container)

	return HttpResponseRedirect(url)

def BayRestore(request,slug,bay):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


	container_list = Container.objects.filter(bayplanfile__slug=slug,bay=bay)
	for  c in container_list:
		if c.stowage != c.original_stowage:
			c.stowage = c.original_stowage
			c.bay = c.original_bay
			c.save()


	# slug = c.bayplanfile.slug
	# bay = c.bay
	url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
	print (url)
	# mode = request.GET.get('mode')
	# if mode=='search':
	# 	query = request.GET.get('q')
	# 	url = reverse('container:bay',kwargs={'slug':slug})
	# 	url = '%s?q=%s' % (url , query)
	# else:
	# 	url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
	# 	# url = '%s?q=%s' % (url , c.container)

	return HttpResponseRedirect(url)

def FileReady(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	action = request.GET.get('action')
	container_list = Container.objects.filter(bayplanfile__slug=slug)
	container_list.update(ready_to_load=True if action=='set' else False)
	# for  c in container_list:
	# 	# if c.stowage != c.original_stowage:
	# 	c.ready_to_load = True if action=='set' else False
	# 	c.save()
	url = reverse('container:bay',kwargs={'slug':slug})
	return HttpResponseRedirect(url)

def BayReady(request,slug,bay):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	action = request.GET.get('action')
	container_list = Container.objects.filter(bayplanfile__slug=slug,bay=bay)
	container_list.update(ready_to_load=True if action=='set' else False)
	# for  c in container_list:
	# 	# if c.stowage != c.original_stowage:
	# 	c.ready_to_load = True if action=='set' else False
	# 	c.save()
	url = reverse('container:bay',kwargs={'slug':slug})
	return HttpResponseRedirect(url)


def BayReport(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	# print(slug)
	query = request.GET.get('q')
	bayfile =BayPlanFile.objects.get(slug=slug)
	c = Container.objects.filter(bayplanfile=bayfile)
	
	if not query :
		# Show Overall view
		b = c.values('bay').annotate(
			number=Count('container'),
			move=Sum(Case(When( stowage = F('original_stowage'),then=Value(0)),default=Value(1),output_field=IntegerField())),
			ready=Sum(Case(When( ready_to_load = True,then=Value(1)),default=Value(0),output_field=IntegerField()))
			)
		dup = c.values('stowage','bay').annotate(number=Count('container')).exclude(number=1)

		return render(
			request,
			'container/bay.html',
			{
			'bays': b,
			'bayfile':bayfile,
			'dups':dup}
			)
	else:
		#show Search result
		# print ('Hello World')
		qs = c.filter(container__icontains=query).order_by('container')
		return render(
			request,
			'container/bay.html',
			{
			'bays': None,
			'bayfile':bayfile,
			'dups':None,
			'container_list':qs}
			)


def BayDetail(request,slug,bay):
	# print(slug,bay)
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	query = request.GET.get('q',None)
	bayfile =BayPlanFile.objects.get(slug=slug)
	c = Container.objects.filter(bayplanfile=bayfile,bay=bay)
	# Find changes slot
	has_changes = False
	b = c.exclude(stowage = F('original_stowage')).count()
	if b > 0 :
		has_changes = True
	# -----------------


	tier = tier1 #Default
	for obj in c:
		stack = obj.stowage[-2:]
		col = obj.stowage[-4:3] if len(obj.stowage)==5 else obj.stowage[-4:4]
		if col=='12' or col=='11' :
			tier = tier2
		# print (obj.stowage,col,stack)

	return render(
		request,
		'container/bay_detail.html',
		{
		'container_list': c,
		'has_change' :has_changes,
		'obj':bayfile,
		'bay': bay,
		'under_deck': under_deck,
		'over_deck':over_deck,
		'tier': tier,
		'q':query}
		)

# filehandle.read()
def FileProcess(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	bayfile =BayPlanFile.objects.get(slug=slug)
	book = xlrd.open_workbook(file_contents=bayfile.filename.read())
	xl_sheet = book.sheet_by_index(0)
	print ('Sheet name: %s' % xl_sheet.name)
	print ('Total row %s' % xl_sheet.nrows )
	print ('Total col %s' % xl_sheet.ncols)

	regex='^[A-Z]{4}[0-9]{7}$'
	item_count =0
	new_count = 0
	Container.objects.filter(bayplanfile=bayfile).delete()
	for row_index in range(1, xl_sheet.nrows):
		vContainer = xl_sheet.cell(row_index, 1).value.__str__().strip()
		if re.match(regex,vContainer):
			item_count = item_count+1
			# Reading all value
			iso 		= xl_sheet.cell(row_index, 2).value.__str__().strip()
			full 		= xl_sheet.cell(row_index, 3).value.__str__().strip()
			partner		= xl_sheet.cell(row_index, 5).value.__str__().strip()
			weight		= xl_sheet.cell(row_index, 6).value.__str__().strip().replace('.0','')
			load_port	= xl_sheet.cell(row_index, 10).value.__str__().strip()
			dis_port	= xl_sheet.cell(row_index, 11).value.__str__().strip()
			delivery_port= xl_sheet.cell(row_index, 12).value.__str__().strip()
			desc        = xl_sheet.cell(row_index, 17).value.__str__().strip()
			stowage		= xl_sheet.cell(row_index, 26).value.__str__().strip().replace('.0','')

			if load_port !='THLCH':
				print ('Not load at LCB %s' % load_port )
				continue

			if len(stowage)==5:
				stowage = '0%s'% stowage
				print (stowage)


			c = Container.objects.create(bayplanfile=bayfile,item_no=item_count,
								container=vContainer,iso_code=iso,full=True if full=='Full' else False,
								partner=partner,weight=weight,
								load_port=load_port,dis_port=dis_port,deliverly_port=delivery_port,
								good_desc=desc,
								stowage=stowage,bay=stowage[:1] if len(stowage)==5 else stowage[:2],
								original_stowage=stowage,original_bay=stowage[:1] if len(stowage)==5 else stowage[:2] )
			# =============
	return redirect(reverse_lazy( 'container:bay', kwargs={'slug': slug}))
	# return render(
	# 	request,
	# 	'container/container_list.html',
	# 	{})