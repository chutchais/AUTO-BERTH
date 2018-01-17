from django.contrib import admin
from .models import Container
# Register your models here.
class ContainerAdmin(admin.ModelAdmin):
    search_fields = ['container']
    list_filter = ['iso_code','load_port','dis_port','deliverly_port']
    list_display = ('__str__','iso_code','load_port','dis_port','deliverly_port')
    # list_editable = ('color','move_performa')
    fieldsets = [
        ('Basic Information',{'fields': ['bayplanfile','container','iso_code','load_port','dis_port','deliverly_port']}),
        ]


admin.site.register(Container,ContainerAdmin)