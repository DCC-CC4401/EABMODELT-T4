from django.shortcuts import render

# Create your views here.
from evaluacion.models import Evaluation


def landingpage(request):
    evaluations = Evaluation.objects.order_by("-date")
    if len(evaluations) > 10:
        evaluations = evaluations[:10]
    return render(request, 'eabmodel/landingpage.html', {'top10_eval': evaluations})
