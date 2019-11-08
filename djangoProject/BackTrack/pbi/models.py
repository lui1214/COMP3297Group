from django.db import models
from django.urls import reverse
from datetime import datetime    
from django.utils import timezone
import datetime
import pytz

# Create your models here.
class Project(models.Model):
	STAT = (
		('Completed', 'Completed'),
		('In Progress', 'In Progress'),
		('Not yet started', 'Not yet started'),
	)
	name = models.CharField(max_length=200)
	description = models.CharField(default='emptyproject', max_length=200)
	status = models.CharField(choices=STAT, default='Not yet started', max_length=200)
	def __str__(self):
		return self.name

class Sprint(models.Model):
	STAT = (
		('Completed', 'Completed'),
		('In Progress', 'In Progress'),
		('Not yet started', 'Not yet started'),
	)
	number = models.IntegerField()
	capacity = models.IntegerField(blank=True, null=True)
	status = models.CharField(choices=STAT, default='Not yet started', max_length=200)
	create_at = models.DateTimeField(blank=True, default=timezone.now, editable=False)
	end_at = models.DateTimeField(blank=True, null=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	
	#def __str__(self):
	#	return self.number
	
	def __str__(self):
		return self.project.name+' Sprint '+str(self.number)

class Item(models.Model):
	STAT = (
		('Completed', 'Completed'),
		('In Progress', 'In Progress'),
		('Not yet started', 'Not yet started'),
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
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return "/pbi/viewPBI/"

class Person(models.Model):
	name = models.CharField(max_length=20)
	def __str__(self):
		return self.name
		
class ProductOwner(Person):
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)

class ScrumMaster(Person):
	role = 'ScrumMaster'

class Developer(Person):
	role = 'Developer'
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)

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
