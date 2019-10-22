from django.db import models

# Create your models here.
class Item(models.Model):
	Description = models.CharField(max_length=200)
	Original_Sprint_Size = models.IntegerField()
	Remaining_Sprint_Size = models.IntegerField()
	Estimate_of_Story_Point = models.IntegerField()
	Status = models.CharField(max_length=200)
	def __str__(self):
		return self.Description