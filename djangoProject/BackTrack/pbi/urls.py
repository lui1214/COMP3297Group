from django.urls import path
from . import views

urlpatterns = [
	path('', 
		views.index, 
		name='index'),
	path('viewPBI/',
		views.PbiView.as_view(),
		name='viewPBI/'),
	path('newPBI/',
		views.PbiCreateView.as_view(),
		name='newPBI'),
	path('updatePBI/<int:pbiUpdate_pk>/',
		views.PbiUpdateView.as_view(),
		name='updatePBI'),
]