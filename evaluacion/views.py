from django.shortcuts import render, HttpResponse
from eabmodel.models import *

# Create your views here.

def index(request):
    return render(request, 'evaluacion/index.html', context={})

def openEval(request):
    return render(request, 'evaluacion/evaluacion.html', context={"completed": False,
                                                                  "team": "EABMODEL Team",
                                                                  "stage": "Tarea 4",
                                                                  "curso": "CC4401-1"})

#@login_required
def openEvalAdmin(request):
    #presenting_group = StudentAtTeam.objects.get(team="eabmodel", active=True)
    return render(request, 'evaluacion/evaluacionadmin.html', context={"completed": False,
                                                                       "group": [["Valentina Pinto", False],
                                                                                 ["José Miguel Cordero", False],
                                                                                 ["José Astorga", False],
                                                                                 ["Juan Saez", True],
                                                                                 ["Tomás Estévez Lenz", True]],
                                                                       "team": "EABMODEL Team",
                                                                       "stage": "Tarea 4"})

def postEval(request):
    return render(request, 'evaluacion/postevaluacion.html', context={"completed": False})

def postEvalAdmin(request):
    return render(request, 'evaluacion/postevaluacionadmin.html', context={"completed": False})
