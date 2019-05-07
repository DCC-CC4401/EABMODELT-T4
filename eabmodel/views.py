from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Course
from django.http import HttpResponseNotFound

from .forms import CourseForm, RemoveCourseForm
# Create your views here.

@login_required
def landingpage(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)


@login_required
def courses(request, extra_context={}):
    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    form = CourseForm()
    course_list = Course.objects.all().order_by('updated_at', 'created_at').reverse()
    context = {'course_list': course_list,
               'form': form,
               }

    context.update(extra_context)
    return render(request, 'eabmodel/course.html', context)


@login_required
def add_course(request):
    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    if request.method != 'POST':
        form = CourseForm()
    else:
        form = CourseForm(request.POST)
        if form.is_valid():
            print(form.data)
            form.save()

    extra_context = {'form': form, 'form_msg': True}
    response = courses(request, extra_context)
    return response


@login_required
def remove_course(request):

    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    if request.method == 'POST':
        form = RemoveCourseForm(request.POST)
        if form.is_valid():
            print("i arrive here")
            course = Course.objects.get(pk=form.cleaned_data['id'])
            course.delete()
    return redirect(reverse('main:courses'))



@login_required
def evaluators(request):
    context = {}
    return render(request, 'eabmodel/landingpage.html', context)


