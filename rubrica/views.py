from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template.defaultfilters import register
from ast import literal_eval
from .models import Rubric
import json


def index(request):
    created_rubrics = Rubric.objects.order_by("-updated_at")
    return render(request, 'rubrica/index.html', {'rubrics': created_rubrics})


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)[1:]


@register.filter(name='clean')
def clean(value):
    return value.split("\', ")[0].split("\'")[-1]


def seeRubric(request, rubric_id):
    rubric = get_object_or_404(Rubric, pk=rubric_id)
    data = literal_eval(rubric.rubric)
    data = {
        "title": rubric.name,
        "table_data": data,
    }
    return render(request, 'rubrica/ver.html', context=data)


def createRubric(request):
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string, encoding='utf-8')
        new_rubric = Rubric.objects.create(
            name=data['name'],
            completed=data['completed'],
            n_compliance_lvl=data['n_compliance_lvl'],
            n_evaluated_aspect=data['n_evaluated_aspect'],
            min_presentation_time=data['min_presentation_time'],
            max_presentation_time=data['max_presentation_time'],
            rubric=json_string
        )
        return HttpResponse(new_rubric.id)

    # empty initial table
    data = {
        "title": "Título",
        "table_data": [["aspecto-tag", "", "", "", ""], ["", "", "", "", ""]]
    }
    return render(request, 'rubrica/modify.html', context=data)


def modifyRubric(request, rubric_id):
    rubric = get_object_or_404(Rubric, pk=rubric_id)
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string, encoding='utf-8')

        # modify rubric fields
        rubric.name = data['name']
        rubric.completed = data['completed']
        rubric.n_compliance_lvl = data['n_compliance_lvl']
        rubric.n_evaluated_aspect = data['n_evaluated_aspect']
        rubric.rubric = json_string
        rubric.save()

        return HttpResponse(rubric_id)

    # load data
    data = literal_eval(rubric.rubric)
    data = {
        "title": rubric.name,
        "table_data": data,
        "min_presentation_time": rubric.min_presentation_time/60.0,
        "max_presentation_time": rubric.min_presentation_time/60.0
    }
    return render(request, 'rubrica/modify.html', context=data)
