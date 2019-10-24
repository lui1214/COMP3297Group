from django.db import models
from django.urls import reverse

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
	cumulative_story_point = models.PositiveIntegerField(default=0)
	status = models.CharField(choices=STAT, default='Not yet started', max_length=200)
		
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return "/pbi/viewPBI/"