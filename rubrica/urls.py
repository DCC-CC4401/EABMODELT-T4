from django.urls import path

from . import views

app_name = 'rubrica'

urlpatterns = [
    path('', views.index, name='index'),
]
