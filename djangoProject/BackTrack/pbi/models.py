from django.db import models
from django.urls import reverse
from datetime import datetime    
from django.utils import timezone
import datetime
import pytz

# Create your models here.
class Item(models.Model):
	STAT = (
		('Completed', 'Completed'),
		('In Progress', 'In Progress'),
		('Not yet started', 'Not yet started'),
	)
	order = models.PositiveIntegerField()
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	original_sprint_size = models.PositiveIntegerField()
	remaining_sprint_size = models.PositiveIntegerField()
	estimate_of_story_point = models.PositiveIntegerField()
	cumulative_story_point = models.PositiveIntegerField(default=0, editable=False)
	status = models.CharField(choices=STAT, default='Not yet started', max_length=200)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True)
	create_at = models.DateTimeField(blank=True, default=timezone.now, editable=False)
	last_sorted = models.DateTimeField(blank=True, editable = False, default=datetime.datetime(1970, 1, 1, 0, 0, 0, 0))
		
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return "/pbi/viewPBI/"

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

class Person(models.Model):
	STAT = (
		('Guest','Guest'),
		('Developer','Developer'),
		('ProductOwner','ProductOwner')
	)
	name = models.CharField(max_length=200)
	role = models.CharField(choices=STAT,default='GUEST',max_length=200)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	def __str__(self):
		return self.name

