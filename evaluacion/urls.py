from django.urls import path

from . import views

app_name = 'evaluacion'

urlpatterns = [
    path('', views.index, name='index'),
    path('eval', views.openEval, name='evaluacion'),
    path('evalAdmin', views.openEvalAdmin, name='evaluacionAdmin'),
    path('postEval', views.postEval, name='postEval'),
    path('postEvalAdmin', views.postEvalAdmin, name='postEvalAdmin'),
]
