from django.shortcuts import render, HttpResponse
from .models import Evaluation

# Create your views here.

def index(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'evaluacion/index.html', {'evaluations': evaluations})
