"""URLs de la aplicación órdenes"""

from django.urls import path
from ordenes import views

urlpatterns = [
	path(
		route='',
		view=views.LoginView.as_view(),
		name='login',
	),
	path(
		route='logout/',
		view=views.LogoutView.as_view(),
		name='logout',
	),
	path(
		route='listado/',
		view=views.ListadoView.as_view(),
		name='listado',
	),
	path(
		route='nuevo/',
		view=views.NuevoView.as_view(),
		name='nuevo',
	),
	path(
		route='ajax/carga_submodulos/',
		view=views.carga_submodulos,
		name='ajax_carga_submodulos'),
]
