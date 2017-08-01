from django.contrib import admin

# Register your models here.
from .models import Terminal,Vessel,Service,Voy

class VoyAdmin(admin.ModelAdmin):
    search_fields = ['voy','code','vessel','service','terminal','vsl_oper','remark']
    list_filter = ['draft','eta','etb','etd','vessel','vsl_oper','service','terminal']
    list_display = ('service','vessel','code','voy','terminal','performa_in','performa_out',
        'eta','etb','etd','dis_no','load_no','est_teu','arrival_draft','vsl_oper')
    fieldsets = [
        ('Basic Information',{'fields': ['voy','slug','code',('service','vessel','vsl_oper'),
        	('terminal','start_pos'),('arrival_draft','departure_draft'),'remark']}),
        ('Performa',{'fields': [('performa_in','performa_out')]}),
        ('Container Information',{'fields': [('dis_no','load_no'),'est_teu']}),
        ('Estimate Time',{'fields': [('eta','etb','etd')]}),
        ('Save as Draft',{'fields': [('draft')]}),
    ]
admin.site.register(Voy,VoyAdmin)




admin.site.register(Service)
admin.site.register(Terminal)
admin.site.register(Vessel)
