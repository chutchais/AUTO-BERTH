from django.forms import ModelForm
from .models import Container
from django import forms
import re

class ContainerForm(ModelForm):
	# bay = forms.CharField(required=False)
	# tier = forms.CharField(required=False)
	# row = forms.CharField(required=False)


	class Meta:
		model = Container
		fields = ['stowage']

	def clean_stowage(self):
		import re
		rex = re.compile("^[0-9]{5,6}$")
		stowage = self.cleaned_data.get("stowage")
		if  len(stowage) < 5 or len(stowage) > 6:
			raise forms.ValidationError('Not a valid Slot , it should be 5 or 6 digit')
		if  not rex.match(stowage):
			raise forms.ValidationError('Not a valid Slot , only accept numeric')
		return stowage

	def __init__(self,stowage=None,*args,**kwargs):
		# voy = kwargs.pop('voy')
		# print(voy_slug)
		# print (voy)
		# print (kwargs)
		# voy = kwargs.pop('voy')
		super(ContainerForm,self).__init__(*args,**kwargs)
		# self.fields['voy'].queryset = Voy.objects.all()

	def save(self, commit=True):
		container = super(ContainerForm, self).save(commit=False)
		print ('Current stowage %s' % container.stowage)
		container.new_stowage = container.stowage
		container.bay=container.stowage[:1] if len(container.stowage)==5 else container.stowage[:2]
		if commit:
			container.save()
		return container