from django.db import models

# Create your models here.
class Item(models.Model):
	order = models.IntegerField()
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	original_sprint_size = models.IntegerField()
	remaining_sprint_size = models.IntegerField()
	estimate_of_story_point = models.IntegerField()
	status = models.CharField(max_length=200)
	def __str__(self):
		return self.name