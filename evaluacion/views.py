from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    return render(request, 'evaluacion/index.html', context={})

def openEval(request):
    return render(request, 'evaluacion/evaluacion.html', context={"completed": False})

def openEvalAdmin(request):
    return render(request, 'evaluacion/evaluacionadmin.html', context={"completed": False})

def postEval(request):
    return render(request, 'evaluacion/postevaluacion.html', context={"completed": False})

def postEvalAdmin(request):
    return render(request, 'evaluacion/postevaluacionadmin.html', context={"completed": False})
