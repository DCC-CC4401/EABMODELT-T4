from django.urls import path
from . import views

app_name = 'rubrica'

urlpatterns = [
    path('', views.index, name='index'),
    path('crear/', views.createRubric, name='crear'),
    path('ver/', views.seeRubric, name='ver'),
    path('modificar/', views.modifyRubric, name='modificar'),
]
