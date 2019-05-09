from django.urls import path, include

from . import views

app_name='main'

urlpatterns = [
    path('contact/', include('contact.urls', namespace='contact')),
    path('', views.landingpage, name='landing_page'),
]
