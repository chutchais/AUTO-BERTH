from django.contrib import admin

# Register your models here.
from .models import Terminal,Vessel,Service,Voy

class VoyAdmin(admin.ModelAdmin):
    search_fields = ['voy','code','vessel__name','service__name','terminal__name','vsl_oper','remark']
    list_filter = ['draft','eta','etb','etd','vessel','vsl_oper','service','terminal']
    list_display = ('service','vessel','code','voy','terminal','performa_in','performa_out',
        'eta','etb','etd','dis_no','load_no','est_teu','arrival_draft','vsl_oper')
    fieldsets = [
        ('Basic Information',{'fields': ['voy','code',('service','vessel','vsl_oper'),
        	('terminal','start_pos'),('arrival_draft','departure_draft'),'remark']}),
        ('Performa',{'fields': [('performa_in','performa_out'),'move_confirm']}),
        ('Container Information',{'fields': [('dis_no','load_no'),'est_teu']}),
        ('Estimate Time',{'fields': [('eta','etb','etd')]}),
        ('Save as Draft',{'fields': [('draft'),'text_pos']}),
    ]
admin.site.register(Voy,VoyAdmin)



class ServiceAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description','color','move_performa','status')
    list_editable = ('color','move_performa')
    fieldsets = [
        ('Basic Information',{'fields': ['name','description','color','move_performa','status']}),
    ]
admin.site.register(Service,ServiceAdmin)

admin.site.register(Terminal)


class VesselAdmin(admin.ModelAdmin):
    search_fields = ['name','imo','description']
    list_filter = ['v_type']
    list_display = ('name','description','lov','imo','color','v_type','status')
    list_editable = ('color',)
    fieldsets = [
        ('Basic Information',{'fields': ['name','description','lov','imo','color','v_type','status']}),
    ]
admin.site.register(Vessel,VesselAdmin)
