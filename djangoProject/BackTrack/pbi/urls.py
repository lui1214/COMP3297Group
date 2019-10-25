from django.urls import path
from . import views

urlpatterns = [
	path('', 
		views.index, 
		name='index'),
	path('viewPBI/',
		views.PbiView.as_view(),
		name='viewPBI'),
	path('createPBI/',
		views.PbiCreateView.as_view(),
		name='createPBI'),
	path('updatePBI/<int:pbiUpdate_pk>/',
		views.PbiUpdateView.as_view(),
		name='updatePBI'),
	path('deletePBI/<int:pbiDelete_pk>/',
		views.PbiDeleteView.as_view(),
		name='deletePBI'),

	path('PersonHomePage/<int:person>/',
		views.PersomHomepage.as_view(),
		name='PersonHomepage'),
]
