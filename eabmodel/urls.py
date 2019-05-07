from django.urls import path

from . import views

app_name='main'

urlpatterns = [
    path('', views.landingpage, name='landing_page'),
    path('courses', views.courses, name='courses'),
    path('add_course', views.add_course, name='add_course'),
    path('rm_course', views.remove_course, name='remove_course'),
    path('evaluators', views.evaluators, name='evaluators'),
    path('add_eval', views.add_eval, name='add_eval'),
    path('rm_eval', views.remove_eval, name='remove_eval'),
]
