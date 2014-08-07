# Create your models here.
from django.contrib.auth import models
from django.db.models import *
from allauth.account.models import EmailAddress
from datetime import datetime

class UserProfile(Model):
	user = OneToOneField(models.User, related_name='profile')
	usertype = ForeignKey('userType', blank=True, null=True, on_delete=SET_NULL)

	def __unicode__(self):
		return "{0}'s profile".format(self.user.username)

	class Meta:
		db_table = 'user_profile'

	def verified(self):
		"""
		If the user is logged in and has verified his/her email address, return True,
		otherwise return False
		"""
		if self.user.is_authenticated:
			result = EmailAddress.objects.filter(email=self.user.email)
			if len(result):
				return result[0].verified
		return False

models.User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class station(Model):
	name = CharField(max_length=32)
	operator = ForeignKey('UserProfile', blank=True, null=True, on_delete=SET_NULL)
	latitude = FloatField(default=0.0)
	longtitude = FloatField(default=0.0)
	status = ForeignKey('status', blank=True, null=True, on_delete=SET_NULL)
		
	def save(self, *args, **kwargs):
		his = station_his(name = self.name, 
						operator = self.operator,
						latitude = self.latitude, 
						longtitude = self.longtitude, 
						status = self.status,
						last_modified_user = kwargs['userobj'].id)
		super(station, self).save()
		his.original_station_id = self
		his.save()
		
	def __unicode__(self):
		return "Station: {0}".format(self.name)


class station_his(Model):
	original_station_id = ForeignKey('station', blank=True, null=True, on_delete=SET_NULL)
	name = CharField(max_length=32)
	operator = ForeignKey('UserProfile', blank=True, null=True, on_delete=SET_NULL)
	latitude = FloatField(default=0.0)
	longtitude = FloatField(default=0.0)
	status = ForeignKey('status', blank=True, null=True, on_delete=SET_NULL)
	last_modified_time = DateTimeField(auto_now=True)
	last_modified_user = IntegerField(blank=True, null=True)
	
	
class device(Model):
	name = CharField(max_length=32)
	station = ForeignKey('station', blank=True, null=True, on_delete=SET_NULL)
	deviceType = ForeignKey('deviceType', blank=True, null=True, on_delete=SET_NULL)
	last_reading_time = DateTimeField(auto_now=True)
	status = ForeignKey('status', blank=True, null=True, on_delete=SET_NULL)
	
	class Meta:
		unique_together = (("name", "station"),)
		
	def __unicode__(self):
		return "Device: {0}".format(self.name)
	
	def save(self, *args, **kwargs):
		his = device_his(name = self.name, 
						station = self.station,
						deviceType = self.deviceType, 
						last_reading_time = self.last_reading_time, 
						status = self.status,
						last_modified_user = kwargs['userobj'].id)
		super(device, self).save()
		his.original_device_id = self
		his.save()

class device_his(Model):
	original_device_id = ForeignKey('device', blank=True, null=True, on_delete=SET_NULL)
	name = CharField(max_length=32)
	station = ForeignKey('station', blank=True, null=True, on_delete=SET_NULL)
	deviceType = ForeignKey('deviceType', blank=True, null=True, on_delete=SET_NULL)
	last_reading_time = DateTimeField(auto_now=True)
	status = ForeignKey('status', blank=True, null=True, on_delete=SET_NULL)
	last_modified_time = DateTimeField(auto_now=True)
	last_modified_user = IntegerField(blank=True, null=True)
	

class following(Model):
	user = ForeignKey('UserProfile', blank=True, null=True, on_delete=SET_NULL)
	station = ForeignKey('station', blank=True, null=True, on_delete=SET_NULL)
	status = ForeignKey('status', blank=True, null=True, on_delete=SET_NULL)

	class Meta:
		unique_together = (("user", "station"),)

	def save(self, *args, **kwargs):
		his = following_his(user = self.user, 
						station = self.station,
						status = self.status,
						last_modified_user = kwargs['userobj'].id)
		super(following, self).save()
		his.original_following_id = self
		his.save()

class following_his(Model):
	original_following_id = ForeignKey('following', blank=True, null=True, on_delete=SET_NULL)
	user = ForeignKey('UserProfile', blank=True, null=True, on_delete=SET_NULL)
	station = ForeignKey('station', blank=True, null=True, on_delete=SET_NULL)
	status = ForeignKey('status', blank=True, null=True, on_delete=SET_NULL)
	last_modified_time = DateTimeField(auto_now=True)
	last_modified_user = IntegerField(blank=True, null=True)


class report(Model):
	device = ForeignKey('device', blank=True, null=True, on_delete=SET_NULL)
	content = CharField(max_length=64)
	reading_time = DateTimeField(default=datetime.now())
	timestamp = DateTimeField(auto_now=True)


class deviceType(Model):
	device_type = CharField(max_length=24)
	unit = CharField(max_length=16)
	
	def __unicode__(self):
		return "Deice Type: {0}, unit:{1}".format(self.device_type,self.unit)


class userType(Model):
	type = CharField(max_length=24)
	
	def __unicode__(self):
		return "User Type: {0}".format(self.type)
	
	
class status(Model):
	status = CharField(max_length=24)

	def __unicode__(self):
		return "Status: {0}".format(self.status)
