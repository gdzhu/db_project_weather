from django.contrib import admin

from project.models import *
# Register your models here.

class stationAdmin(admin.ModelAdmin):
	model = station
	list_display = ('id', 'name', 'operator', 'latitude', 'longtitude', 'status')
	
	def save_model(self, request, obj, form, change): 
		obj.save(userobj = request.user)

	def save_formset(self, request, form, formset, change): 
			instances = formset.save(commit=False)
			for instance in instances:
				instance.save(userobj = request.user)


class deviceAdmin(admin.ModelAdmin):
	model = device
	list_display = ('id', 'name', 'station', 'deviceType', 'last_reading_time', 'status')
	def save_model(self, request, obj, form, change): 
		obj.save(userobj = request.user)

	def save_formset(self, request, form, formset, change): 
			instances = formset.save(commit=False)
			for instance in instances:
				instance.save(userobj = request.user)
				
				
class followingAdmin(admin.ModelAdmin):
	model = following
	list_display = ('id', 'user', 'station', 'status')
	
	def save_model(self, request, obj, form, change): 
		obj.save(userobj = request.user)

	def save_formset(self, request, form, formset, change): 
			instances = formset.save(commit=False)
			for instance in instances:
				instance.save(userobj = request.user)
				
				
class deviceTypeAdmin(admin.ModelAdmin):
	model = deviceType
	list_display = ('id', 'device_type', 'unit')

class reportAdmin(admin.ModelAdmin):
	model = report
	list_display = ('id', 'device', 'content', 'timestamp')

class userTypeAdmin(admin.ModelAdmin):
	model = userType
	list_display = ('id', 'type')

class statusAdmin(admin.ModelAdmin):
	model = status
	list_display = ('id', 'status')


# admin.site.register(user, userAdmin)
admin.site.register(UserProfile)
admin.site.register(station, stationAdmin)
admin.site.register(station_his)
admin.site.register(device, deviceAdmin)
admin.site.register(device_his)
admin.site.register(following, followingAdmin)
admin.site.register(following_his)
admin.site.register(deviceType, deviceTypeAdmin)
admin.site.register(report, reportAdmin)
admin.site.register(userType, userTypeAdmin)
admin.site.register(status, statusAdmin)
