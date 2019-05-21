from django.urls import path, include

from . import views

app_name='main'

urlpatterns = [
    path('contact/', include('contact.urls', namespace='contact')),
    path('evaluaciones/', include('evaluacion.urls', namespace='evaluaciones')),
    path('rubricas/', include('rubrica.urls', namespace='rubricas')),
    path('', views.landingpage, name='landing_page'),
]
