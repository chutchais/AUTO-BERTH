from django.contrib import admin
from .models import Container
# Register your models here.
class ContainerAdmin(admin.ModelAdmin):
    search_fields = ['container']
    list_filter = ['iso_code','load_port','dis_port','deliverly_port']
    list_display = ('__str__','ready_to_load','uploaded','iso_code','load_port','dis_port','deliverly_port')
    # list_editable = ('color','move_performa')
    fieldsets = [
        ('Basic Information',{'fields': ['bayplanfile','container','slug','ready_to_load',
        	'uploaded','upload_date','iso_code','load_port','dis_port','deliverly_port',
        	'stowage','original_stowage']}),
        ]


admin.site.register(Container,ContainerAdmin)