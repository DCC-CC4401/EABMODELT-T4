from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseNotFound

from users.models import EvaluatorUser
from users.forms import EvaluatorUserCreationForm, EvaluatorUserRemoveForm, EvaluatorUserChangeForm

from .models import Course
from .forms import CourseForm, RemoveCourseForm, ModifyCourseForm


# Create your views here.
from evaluacion.models import Evaluation


@login_required
def landingpage(request):
    evaluations = Evaluation.objects.order_by("-date")
    if len(evaluations) > 10:
        evaluations = evaluations[:10]
    return render(request, 'eabmodel/landingpage.html', {'top10_eval': evaluations})


@login_required
def courses(request, extra_context={}):
    context = {'is_admin': False}

    if not request.user.is_admin:
        course_list = Course.objects.all().filter(evaluators=request.user).order_by('updated_at', 'created_at').reverse()

    else:
        form = CourseForm(prefix='agregar')
        course_list = Course.objects.all().order_by('updated_at', 'created_at').reverse()
        context.update({'form': form, 'is_admin': True})

    context.update({'course_list': course_list, 'modify_form': ModifyCourseForm(prefix="modificar")})

    context.update(extra_context)
    return render(request, 'eabmodel/course.html', context)


@login_required
def add_course(request):
    extra_context = {}

    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    if request.method != 'POST':
        form = CourseForm(prefix="agregar")

    else:
        form = CourseForm(request.POST, prefix="agregar")
        if form.is_valid():
            added_course = form.save()
            extra_context.update({'added_course': added_course, 'added_msg': True})
# form
    extra_context.update({'form': form})
    response = courses(request, extra_context)
    return response

@login_required
def modify_course(request, course=None):
    extra_context ={}

    if course is not None:
        if not request.user.is_admin:
            return HttpResponseNotFound('Sorry')

        if request.method == 'POST':
            new_form = ModifyCourseForm(request.POST, instance=Course.objects.get(pk=course), prefix="modificar",)

            if new_form.is_valid():
                new_form.save()

            extra_context.update({'modify_form': new_form})

    response = courses(request, extra_context)
    return response



@login_required
def remove_course(request):

    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    if request.method == 'POST':
        form = RemoveCourseForm(request.POST)
        if form.is_valid():
            course = Course.objects.get(pk=form.cleaned_data['id'])
            course.delete()
    return redirect(reverse('main:courses'))



@login_required
def evaluators(request, extra_context={}):

    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    form = EvaluatorUserCreationForm()

    evaluator_list = EvaluatorUser.objects.all()\
        .filter(is_active=True)\
        .exclude(pk=request.user.id)\
        .order_by('date_joined')\
        .reverse()

    context = {'evaluator_list': evaluator_list,
               'form': form,
               'modify_form': EvaluatorUserChangeForm(prefix="modificar")
               }

    context.update(extra_context)
    return render(request, 'eabmodel/evaluator.html', context)


@login_required
def add_eval(request):

    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    extra_context = {}
    if request.method != 'POST':
        form = EvaluatorUserCreationForm()
    else:
        form = EvaluatorUserCreationForm(request.POST)

        if form.is_valid():
            evaluator = form.save(commit=False)
            password = EvaluatorUser.objects.make_random_password()
            evaluator.set_password(password)
            evaluator.save()

            extra_context.update({'password': password, 'added_user': evaluator, "added_msg":True})
            form = EvaluatorUserCreationForm() # clean the form

    extra_context.update({'form': form})
    response = evaluators(request, extra_context)
    return response


@login_required
def remove_eval(request):

    if not request.user.is_admin:
        return HttpResponseNotFound("I don't know how you get here :s")

    if request.method == 'POST':
        form = EvaluatorUserRemoveForm(request.POST)
        if form.is_valid():
            evaluator = EvaluatorUser.objects.get(pk=form.cleaned_data['id'])
            evaluator.delete()
    return redirect(reverse('main:evaluators'))


@login_required
def modify_eval(request, eval=None):
    extra_context = {}

    if eval is not None:
        if not request.user.is_admin:
            return HttpResponseNotFound('Sorry')

        if request.method == 'POST':
            new_form = EvaluatorUserChangeForm(request.POST, instance=EvaluatorUser.objects.get(pk=eval), prefix="modificar" )
            if new_form.is_valid():
                new_form.save()
            extra_context.update({'modify_form': new_form})

    response = evaluators(request, extra_context)
    return response


