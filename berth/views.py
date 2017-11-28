from django.shortcuts import render

# Create your views here.
# from pdfdocument.utils import pdf_response 
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
import os.path
from django.conf import settings

from .models import ReportFile,Voy,cutoff

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import CutoffForm

class VoyDetailView(DetailView):
	model = Voy

class CutOffDetailView(DetailView):
	model = cutoff

class CutOffUpdateView(LoginRequiredMixin,UpdateView):
	model = cutoff
	template_name = 'berth/cutoff_detail_update.html'
	form_class = CutoffForm

	def get_queryset(self):
		qs = super(CutOffUpdateView, self).get_queryset()
		return qs.all()

	def get_form_kwargs(self):
		kwargs = super(CutOffUpdateView,self).get_form_kwargs()
		print(kwargs)
		return kwargs

class CutOffCreateView(LoginRequiredMixin,CreateView):
	# model = cutoff
	template_name = 'form.html'
	form_class = CutoffForm

	def form_valid(self,form):
		obj = form.save(commit=False)
		return super(CutOffCreateView,self).form_valid(form)

	def get_initial(self):
		voy = get_object_or_404(Voy, slug=self.kwargs.get('slug'))
		return {'voy':voy}

	def get_form_kwargs(self):
		kwargs = super(CutOffCreateView,self).get_form_kwargs()
		# kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
		return kwargs

	# # def get_queryset(self):
	# # 	return Item.objects.filter(user=self.request.user)
	def get_queryset(self):
		qs = super(CutOffUpdateView, self).get_queryset()
		return qs.filter(voy__vessel__v_type='VESSEL')

	def get_context_data(self,*args,**kwargs):
		context = super(CutOffCreateView,self).get_context_data(*args,**kwargs)
		context['title']='Add Cut-Off Datetime'
		return context

class CutOffDeleteView(LoginRequiredMixin,DeleteView):
	model = cutoff
	success_url = reverse_lazy('berth:cutoff-home')


# def xls_to_response(xls, fname):
#     response = HttpResponse(mimetype="application/ms-excel")
#     response['Content-Disposition'] = 'attachment; filename=%s' % fname
#     xls.save(response)
#     return response


# def index(request):
#     response = HttpResponse(mimetype="application/ms-excel")
#     response['Content-Disposition'] = 'attachment; filename=test.xlsm'
#     xls.save(response)
#     return response
def index(request):
	reports = ReportFile.objects.all().order_by('-modified_date')
	return render(request, 'index.html', {'objs': reports})




def pdf_view(request):
	vFileName ='test.pdf'
	full_path = os.path.join(settings.STATIC_ROOT, vFileName) #static(vFileName)
	with open(full_path, 'rb') as pdf:
		response = HttpResponse(pdf.read(),content_type='application/pdf')
		response['Content-Disposition'] = 'filename=some_file.pdf'
	return response
	# pdf, response = pdf_response('filename_without_extension')
	# # ... more code
	# pdf.generate()
	# return HttpResponse(full_path)


# Add by Chutchai on Nov 23,2017
# to Show Auto Cut-off datetime
def foo(year, week):
	from datetime import date, timedelta
	d = date(year,1,1)
	dlt = timedelta(days = ((week-1)*7)+1)
	return d + dlt ,  d + dlt + timedelta(days=7)

def cutoff(request):
	from django.db.models import Q
	# from datetime import datetime
	import datetime
	from datetime import timedelta
	# import datetime
	year = request.GET.get('year', '')
	workweek = request.GET.get('week', '')
	if workweek=='' and year=='':
		# Use current week
		today= datetime.date.today()
		from_date = today -  timedelta(days=today.weekday())
		to_date = from_date +  timedelta(days=7)
		year = from_date.strftime('%Y')#-%m-%d %H:%M
		workweek = from_date.strftime('%W')
	else:
		# from isoweek import Week
		d = foo(int(year),int(workweek))
		from_date = d[0]
		to_date = d[1]
		print(d)
	# wk = from_date.isocalendar()[1]
	# ------------

	b = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		# Q(etd__range=[from_date,to_date]),
		terminal='B1',
		vessel__v_type='VESSEL',
		draft=False).exclude(service__name__icontains='DIS').order_by('etb')


	a = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		# Q(etd__range=[from_date,to_date]),
		terminal__name__icontains ='A',
		vessel__v_type='VESSEL',
		draft=False).exclude(
			service__name__icontains='DIS'
		).order_by('etb')

	# last = Voy.objects.filter(
	# 	Q(etb__range=[from_date,to_date]),
	# 	vessel__v_type='VESSEL',
	# 	draft=False).exclude(service__name__icontains='DIS').order_by('etb').aggregate(Max('price'))
	

	return render(request, 'cutoff.html', {'A':a,
						'B':b,
						'year':year,
						'week':workweek})