from django.urls import path

from . import views

app_name='main'

urlpatterns = [
    path('', views.landingpage, name='landing_page'),
]
