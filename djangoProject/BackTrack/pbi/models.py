from django.db import models
from django.urls import reverse
from datetime import datetime	
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
import datetime
import pytz
import uuid
import hashlib
import os
import time

def _hash():
	hash = hashlib.sha1()
	hash.update(str(time.time()).encode('utf-8'))
	hash.update(uuid.uuid1().hex.encode('utf-8'))
	return hash.hexdigest()

class Project(models.Model):
	STAT = (
		('Completed', 'Completed'),
		('In Progress', 'In Progress'),
		('Not yet started', 'Not yet started'),
	)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	status = models.CharField(choices=STAT, default='Not yet started', max_length=200)
	last_sprint = models.IntegerField(default=1, editable=False)
	Dhash = models.CharField(max_length=200, default=_hash, editable=False)
	SMhash = models.CharField(max_length=200, default=_hash, editable=False)
	
	def __str__(self):
		return self.name

class Person(models.Model):
	STAT = (
		('Product Owner', 'Product Owner'),
		('Scrum Master', 'Scrum Master'),
		('Developer', 'Developer'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	role = models.CharField(choices=STAT, max_length=200, blank=True, null=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
	
	def __str__(self):
		return self.user.username

class Sprint(models.Model):
	STAT = (
		('Completed', 'Completed'),
		('In Progress', 'In Progress'),
		('Not yet started', 'Not yet started'),
	)
	number = models.IntegerField(blank=True, null=True)
	capacity = models.IntegerField(blank=True, null=True)
	status = models.CharField(choices=STAT, default='Not yet started', max_length=200)
	create_at = models.DateTimeField(blank=True, default=timezone.now, editable=False)
	end_at = models.DateTimeField(blank=True, null=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
	
	#def __str__(self):
	#	return self.number
	
	def __str__(self):
		return self.project.name+' Sprint '+str(self.number)

class Item(models.Model):
	STAT = (
		('Completed', 'Completed'),
		('In Progress', 'In Progress'),
		('Not yet started', 'Not yet started'),
		('Not finished', 'Not finished'),
	)
	order = models.PositiveIntegerField()
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	remaining_sprint_size = models.PositiveIntegerField()
	estimate_of_story_point = models.PositiveIntegerField()
	cumulative_story_point = models.PositiveIntegerField(default=0, editable=False)
	status = models.CharField(choices=STAT, default='Not yet started', max_length=200)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True)
	create_at = models.DateTimeField(blank=True, default=timezone.now, editable=False)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
	sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, blank=True, null=True)
	added = models.BooleanField(default=False, editable=False)
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return "/pbi/viewPBI/"

class Task(models.Model):
	STAT = (
		('Completed', 'Completed'),
		('In Progress', 'In Progress'),
		('Not yet started', 'Not yet started'),
	)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	hour = models.PositiveIntegerField(blank=True, null=True)
	status = models.CharField(choices=STAT, default='Not yet started', max_length=200)
	create_at = models.DateTimeField(blank=True, default=timezone.now, editable=False)
	item = models.ForeignKey(Item,on_delete=models.CASCADE,blank=True, null=True)
	sprint = models.ForeignKey(Sprint,on_delete=models.CASCADE,blank=True, null=True)
	person = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
	
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		tsprint=self.sprint
		return "/pbi/viewTask/%i/" % self.id
