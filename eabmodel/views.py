from django.shortcuts import render


# Create your views here.
def landingpage(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)


def courses(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)


def evaluators(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)
