from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_ejercicio, name='ejercicio'),
    path('resolucion/', views.get_resolucion, name='resolucion'),
    path('resolucion_parametrizable/', views.resolucion_parametrizable, name='resolucion_parametrizable'),
]
