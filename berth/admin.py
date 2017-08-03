from django.contrib import admin

# Register your models here.
from .models import Terminal,Vessel,Service,Voy


from datetime import date
from django.utils.translation import gettext_lazy as _
# from django import forms
# from .models import Voy


class ETAListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('ETA range')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'eta'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('today', _('Today')),
            ('thisweek', _('This week')),
            ('nextweek', _('Next week')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        from datetime import date
        if self.value() == 'today':
            today = date.today()
            return queryset.filter(eta__year=today.year,eta__month=today.month,eta__day=today.day).order_by('eta')
        if self.value() == 'thisweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(eta__range=[start_week, end_week]).order_by('eta')

        if self.value() == 'nextweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            date = end_week + datetime.timedelta(days=1)
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(eta__range=[start_week, end_week]).order_by('eta')

class ETBListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('ETB range')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'etb'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('today', _('Today')),
            ('thisweek', _('This week')),
            ('nextweek', _('Next week')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        from datetime import date
        if self.value() == 'today':
            today = date.today()
            return queryset.filter(etb__year=today.year,etb__month=today.month,etb__day=today.day).order_by('etb')
        if self.value() == 'thisweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(etb__range=[start_week, end_week]).order_by('etb')

        if self.value() == 'nextweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            date = end_week + datetime.timedelta(days=1)
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(etb__range=[start_week, end_week]).order_by('etb')

class ETDListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('ETD range')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'etd'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('today', _('Today')),
            ('thisweek', _('This week')),
            ('nextweek', _('Next week')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        from datetime import date
        if self.value() == 'today':
            today = date.today()
            return queryset.filter(etd__year=today.year,etd__month=today.month,etd__day=today.day).order_by('etd')
        if self.value() == 'thisweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(etd__range=[start_week, end_week]).order_by('etd')

        if self.value() == 'nextweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            date = end_week + datetime.timedelta(days=1)
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(etd__range=[start_week, end_week]).order_by('etd')


# class VoyForm(forms.ModelForm):
#     class Meta:
#         model = Voy

#     def clean(self):
#         etb_date = self.cleaned_data.get('etb')
#         etd_date = self.cleaned_data.get('etd')
#         if start_date >= end_date:
#             raise forms.ValidationError("ETD date must be Bigger than ETB")
#         return self.cleaned_data

class VoyAdmin(admin.ModelAdmin):
    search_fields = ['voy','code','vessel__name','service__name','terminal__name','vsl_oper','remark']
    list_filter = ['terminal','vessel__v_type',ETAListFilter,ETBListFilter,ETDListFilter,'draft','vessel','vsl_oper','service']
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
