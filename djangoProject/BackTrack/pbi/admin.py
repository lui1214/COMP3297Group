from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
from .models import *
admin.site.register(Item)
admin.site.register(Person)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Task)
