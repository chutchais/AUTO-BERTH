from django.contrib import admin

from .models import BayPlanFile
# Register your models here.

class BayPlanFileAdmin(admin.ModelAdmin):
    search_fields = ['filename','voy__voy','voy__vessel__name']
    list_filter = ['uploaded','voy__vessel']
    list_display = ('__str__','created_date','uploaded','upload_date')
    # list_editable = ('color','move_performa')
    fieldsets = [
        ('Basic Information',{'fields': ['filename','remark','uploaded','upload_date']}),
    ]
admin.site.register(BayPlanFile,BayPlanFileAdmin)

# admin.site.register(BayPlanFile)
