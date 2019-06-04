from django.urls import path
from . import views

app_name = 'rubrica'

urlpatterns = [
    path('', views.index, name='index'),
    path('crear/', views.createRubric, name='crear'),
    path('<int:rubric_id>/ver/', views.seeRubric, name='ver'),
    path('<int:rubric_id>/rm/', views.rm_rubric, name='remover'),
    path('<int:rubric_id>/modificar/', views.modifyRubric, name='modificar'),
]
