from django.forms import ModelForm
from .models import cutoff,Voy

class CutoffForm(ModelForm):
	class Meta:
		model = cutoff
		fields = ['voy','dry_date','reef_date','chilled_date','durian_date']

	def __init__(self,voy=None,*args,**kwargs):
		print (voy)
		print (kwargs)
		super(CutoffForm,self).__init__(*args,**kwargs)
		# self.fields['voy'] = Voy.objects.all()