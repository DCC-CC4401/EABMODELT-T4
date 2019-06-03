from django.urls import path, include

from . import views

app_name='main'

urlpatterns = [
    path('contact/', include('contact.urls', namespace='contact')),
    path('evaluaciones/', include('evaluacion.urls', namespace='evaluaciones')),
    path('rubricas/', include('rubrica.urls', namespace='rubricas')),
    path('', views.landingpage, name='landing_page'),

    path('courses', views.courses, name='courses'),
    path('add_course', views.add_course, name='add_course'),
    path('rm_course', views.remove_course, name='remove_course'),
    path('modify_course', views.modify_course, name='modify_course'),
    path('modify_course/<int:course>', views.modify_course, name='modify_course'),

    path('evaluators', views.evaluators, name='evaluators'),
    path('modify_eval', views.modify_eval, name='modify_eval'),
    path('modify_eval/<int:eval>', views.modify_eval, name='modify_eval'),
    path('add_eval', views.add_eval, name='add_eval'),
    path('rm_eval', views.remove_eval, name='remove_eval'),
]
