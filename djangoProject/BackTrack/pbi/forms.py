from django.forms import ModelForm
from pbi.models import Item, Person
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ItemForm(ModelForm):
	class Meta:
		model = Item
		fields = '__all__'

class RegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]