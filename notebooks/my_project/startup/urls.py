from django.urls import path

from . import views

urlpatterns = [

	#path('indexer/', views.startup, name='indexer'),
	path('', views.main, name='main'),
	path('listing/', views.lister, name='lister'),
	path('listing/details/<int:id>', views.details, name='details'),
	path('testing/', views.testing, name='testing'),
]
