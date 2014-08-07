# encoding=UTF-8
from django import template

register = template.Library()


def get_val(dict, key):
	print('looking up '+str(key) + ' in ' + str(dict))
	if str(key) in dict:
		print('found it')
		return dict[str(key)]
	else: 
		print('did not find it')
		return 

register.filter('get_val', get_val)

def status_label_color(status_str):
	if (status_str == 'online'):
		return 'success'
	elif (status_str == 'inactive'):
		return 'warning'
	elif (status_str == 'offline'):
		return 'error'
	else:
		return 'danger'

register.filter('status_label_color', status_label_color)

def float_to_latlong(f_val, latlong):
	latlongStr = str(int(f_val)) + "°"+ str(int((f_val-int(f_val))*100))+"'"
	if (latlong=="latitude"):
		if (f_val >= 0): 
			latlongStr +=" N"
		else:
			latlongStr +=" S"
	elif (latlong=="longitude"): 
		if (f_val >= 0): 
			latlongStr +=" E"
		else:
			latlongStr +=" W"
	else:
		latlongStr += "??"

	return latlongStr

register.filter('float_to_latlong', float_to_latlong)
