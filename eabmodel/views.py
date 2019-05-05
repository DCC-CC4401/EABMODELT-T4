from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def landingpage(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)


@login_required
def courses(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)


@login_required
def evaluators(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)
