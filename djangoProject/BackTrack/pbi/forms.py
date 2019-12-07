from django.forms import ModelForm
from pbi.models import Item, Person
from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User

class ItemForm(ModelForm):
	class Meta:
		model = Item
		fields = '__all__'

class RegisterForm(UserCreationForm):

	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]
        
class JoinProjectForm(forms.Form):
    field = forms.CharField(label='Hashkey', max_length=80)