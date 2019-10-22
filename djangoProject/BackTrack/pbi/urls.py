from django.urls import path
from pbi import views

urlpatterns = [
	path('customerOrders/<int:customer>',
		views.CustomerViewOrders.as_view(),
		name='customer-orders'),
]