from django.urls import path
from . import views

urlpatterns = [
	path('', 
		views.index, 
		name='index'),
	path('viewPBIdetail/<int:item>/',
		views.PbiDetailView.as_view(),
		name='viewPBIdetail'),
	path('viewPBI/',
		views.PbiView.as_view(),
		name='viewPBI'),
	path('viewCurrentPBI/',
		views.PbiCurrentView.as_view(),
		name='viewCurrentPBI'),
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
		name='PersonHomepage')
]
