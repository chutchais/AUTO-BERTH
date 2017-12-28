from django import forms
from django.forms import ModelForm

from .models import BayPlanFile

class BayPlanForm(ModelForm):
	class Meta:
		model = BayPlanFile
		fields =[
			'filename',
			'remark',
		]
	def __init__(self,user=None,*args,**kwargs):
		super(BayPlanForm,self).__init__(*args,**kwargs)
		# self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user) #.exclude(item__isnull=False)