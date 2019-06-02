from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Rubric
from rubrica.utils import rubric_to_table
import json


def index(request):
    return render(request, 'rubrica/index.html', context={})


def seeRubric(request, rubric_id):
    rubric = get_object_or_404(Rubric, pk=rubric_id)
    data = json.loads(rubric.rubric, encoding='uft-8')

    data = {
        "title": rubric.name,
        "table_data": rubric_to_table(data["rubric"]),
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
        print(new_rubric.id)
        print(json_string)
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
        print(json_string)
        rubric.save()

        return HttpResponse(rubric_id)

    # load data
    data = json.loads(rubric.rubric, encoding='uft-8')
    data = {
        "title": rubric.name,
        "table_data": rubric_to_table(data["rubric"]),
        "min_presentation_time": rubric.min_presentation_time/60.0,
        "max_presentation_time": rubric.min_presentation_time/60.0
    }
    return render(request, 'rubrica/modify.html', context=data)
