from django import template
from datetime import timedelta
import datetime

register = template.Library()

# @register.filter(name='cut')
# def cut(value, arg):
#     return value.replace(arg, '')

# @register.filter
# def lower(value):
#     return value.lower()

# @register.filter
# def in_repair(obj):
#     return obj.all().exclude(status='CLOSED')


@register.assignment_tag
def cut(service):
	return service.__str__().split('-')[0]


@register.assignment_tag
def is_arrive(etb):
	if etb < datetime.datetime.now():
		return 'Arrived'
	else:
		return '...'


@register.assignment_tag
def is_fix_cutoff(service):
	strService = service.__str__().split('-')[0]
	service_lists = ['BOOM','HORN','SE1','ANX','TR1','NTX','PH4','IA2','THAI2']#{'BOOM','HORN','SE1','ANX'.'TR1','NTX','PH4','IA2'}
	if strService in  service_lists :
		# print(service)
		return True

@register.assignment_tag
def is_overdue(perform_date):
	import datetime
	now = datetime.datetime.now()
	# print (now)
	# return True
	if perform_date < now:
		# print ('Over')
		return 'class=danger'

@register.assignment_tag
def set_to_Saturday(service,perform_date):
	strService = service.__str__()
	firstday = perform_date -  timedelta(days=perform_date.weekday())
	Saturday = firstday + datetime.timedelta( (5-firstday.weekday()) % 7 )
	if 'BOOM' in strService :
		return Saturday.replace(hour=5, minute=00)

	if 'HORN' in strService :
		return Saturday.replace(hour=12, minute=00)


@register.assignment_tag
def decrease_hour(date_in,hour):
	return date_in - timedelta(hours=hour)


@register.assignment_tag
def increase_hour(date_in,hour):
	return date_in + timedelta(hours=hour)


@register.assignment_tag
# ['BOOM','HORN','SE1','ANX'.'TR1','NTX','PH4','IA2']
def get_fix_cutoff(service,perform_date):
	strService = service.__str__()
	firstday = perform_date -  timedelta(days=perform_date.weekday())
	Monday = firstday + datetime.timedelta( (0-firstday.weekday()) % 7 )
	Tueday = firstday + datetime.timedelta( (1-firstday.weekday()) % 7 )
	Wednesday = firstday + datetime.timedelta( (2-firstday.weekday()) % 7 )
	Thursday = firstday + datetime.timedelta( (3-firstday.weekday()) % 7 )
	Friday = firstday + datetime.timedelta( (4-firstday.weekday()) % 7 )
	Saturday = firstday + datetime.timedelta( (5-firstday.weekday()) % 7 )
	Sunday = firstday + datetime.timedelta(days=6) #datetime.timedelta( (6-firstday.weekday()) % 7 )
	# print ('Get Fix %s' % strService)
	if 'BOOM' in strService :
		return Saturday.replace(hour=5, minute=00)

	if 'HORN' in strService :
		return Saturday.replace(hour=12, minute=00)

	if 'SE1' in strService :
		print (Thursday)
		return Thursday.replace(hour=6, minute=00)

	if 'ANX' in strService :
		return Tueday.replace(hour=23, minute=59)

	if 'TR1' in strService :
		return Thursday.replace(hour=11, minute=00)

	if 'NTX' in strService :
		return Friday.replace(hour=18, minute=00)

	if 'PH4' in strService :
		return Saturday.replace(hour=2, minute=00)

	if 'IA2' in strService :
		# print('IA2 %s' % firstday)
		return Sunday.replace(hour=14, minute=00)

	if 'THAI2' in strService :
		# print('THAI2 %s' % firstday)
		return perform_date - datetime.timedelta(hours=12)



# @register.assignment_tag
# def strip(obj):
# 	# print (obj.strip())
# 	return obj.strip()

# @register.assignment_tag
# def is_boi(obj,machine):
# 	# print (obj.strip())
# 	return True if obj.strip() in machine.values_list('machine_name',flat=True) else False


# @register.assignment_tag
# def combine_date(year,month,day):
# 	# print (obj.strip())
# 	return ('%s-%s-%s' % (year,month,day))

def add( value, arg ):
	'''
	Divides the value; argument is the divisor.
	Returns empty string on any error.
	'''
	try:
	    value = int( value )
	    arg = int( arg )
	    if arg: return value + arg
	except: pass
	return ''
