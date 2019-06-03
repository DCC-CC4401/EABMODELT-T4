from django.urls import path

from . import views

app_name = 'evaluacion'

urlpatterns = [
    path('', views.index, name='index'),
    path('eval/<str:name>/<str:course>/<str:section>/<str:semester>/<str:year>/<str:team>', views.openEval, name='evaluacion'),
    path('evalAdmin/<str:name>/<str:course>/<str:section>/<str:semester>/<str:year>/<str:team>', views.openEvalAdmin, name='evaluacionAdmin'),
    path('postEval/<str:name>/<str:course>/<str:section>/<str:semester>/<str:year>/<str:team>', views.postEval, name='postEval'),
    path('postEvalAdmin/<str:name>/<str:course>/<str:section>/<str:semester>/<str:year>/<str:team>', views.postEvalAdmin, name='postEvalAdmin'),
    path('<int:id>/addEvaluator/', views.add_evaluator_view, name='addevaluator'),
 	path('<int:id>/editRubric/', views.edit_rubric, name='editRubric'),
 	path('<int:id>/editDates/', views.edit_dates, name='editDates'),
]
