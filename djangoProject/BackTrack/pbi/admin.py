from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Item)
admin.site.register(Person)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Task)
