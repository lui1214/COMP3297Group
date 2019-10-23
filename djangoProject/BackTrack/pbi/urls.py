from django.urls import path
from pbi import views

urlpatterns = [
	path('pbi/',
		views.PbiView.as_view(),
		name='pbi'),
]