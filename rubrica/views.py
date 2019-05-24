from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Rubric
from rubrica.utils import rubric_to_table
import json


def index(request):
    return render(request, 'rubrica/index.html', context={})


def seeRubric(request, rubric_id=47):
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
            # suggested_presentation_time=data['suggested_presentation_time'],
            completed=data['completed'],
            n_compliance_lvl=data['n_compliance_lvl'],
            n_evaluated_aspect=data['n_evaluated_aspect'],
            # created_at=1,
            # updated_at=1,
            rubric=json_string
        )
        return HttpResponse(new_rubric.id)

    # empty initial table
    data = {
        "title": "Título",
        "table_data": [["", "", "", "", ""], ["", "", "", "", ""]]
    }
    return render(request, 'rubrica/modify.html', context=data)


def modifyRubric(request, rubric_id=47):
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
        return HttpResponse(json_string)

    # load data
    data = json.loads(rubric.rubric, encoding='uft-8')
    data = {
        "title": rubric.name,
        "table_data": rubric_to_table(data["rubric"]),
    }
    return render(request, 'rubrica/modify.html', context=data)
