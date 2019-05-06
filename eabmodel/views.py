from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course
from django.http import HttpResponseNotFound

from .forms import CourseForm
# Create your views here.

@login_required
def landingpage(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)


@login_required
def courses(request):
    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    course_list = Course.objects.all().order_by('updated_at', 'created_at').reverse()
    context = {'course_list': course_list,
               # 'form': form,
               }
    return render(request, 'eabmodel/course.html', context)


@login_required
def add_course(request):
    if request.method != 'POST':
        form = CourseForm()
    else:
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'eabmodel/add_course.html', {'form': form})

@login_required
def evaluators(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)


