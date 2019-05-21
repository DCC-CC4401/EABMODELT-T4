from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Rubric
import json


# Create your views here.


def index(request):
    return render(request, 'rubrica/index.html', context={})


def seeRubric(request, rubric_id=36):
    # TODO crear contexto a partir de rubric_id
    rubric = get_object_or_404(Rubric, pk=rubric_id)
    data = json.loads(rubric.rubric, encoding='uft-8')
    print(data["rubric"])
    # context={'data':data}
    data = {}
    return render(request, 'rubrica/ver.html', context=data)


def createRubric(request):
    # TODO crear contexto vacío
    if request.method == 'POST':
        # TODO crear/parsear json, agregar modelo a la bd, mostrar pagina de "logrado"
        json_string = request.POST.get("json")
        data = json.loads(json_string, encoding='uft-8')
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
        #return HttpResponse(json_string)
        data = {"success_alert" : True}
        return render(request, 'rubrica/modify.html', context=data)

    # empty initial table
    data = {"table_data": [[("0-0", ""), ("0-1", ""), ("0-2", ""), ("0-3", "")],
                           [("1-0", ""), ("1-1", ""), ("1-2", ""), ("1-3", "")]],
            "success_alert": False,
            "title" : "Título"
            }
    return render(request, 'rubrica/modify.html', context=data)


def modifyRubric(request, rubric_id=36):
    rubric = get_object_or_404(Rubric, pk=rubric_id)
    # TODO crear contexto a partir de rubric_id
    if request.method == 'POST':
        # TODO crear/parsear json, agregar modelo a la bd, mostrar pagina de "logrado"
        json_string = request.POST.get("json")
        data = json.loads(json_string, encoding='uft-8')
        rubric.name = data['name']
        rubric.completed = data['completed']
        rubric.n_compliance_lvl = data['n_compliance_lvl']
        rubric.n_evaluated_aspect = data['n_evaluated_aspect']
        rubric.rubric = json_string
        return HttpResponse(json_string)

    data = json.loads(rubric.rubric, encoding='uft-8')
    table = []
    for i in range(len(data["rubric"])):
        row = []
        for j in range(len(data["rubric"][i])):
            cell_name = str(i) + "-" + str(j)
            cell_content = data["rubric"][i][cell_name]
            row.append((cell_name, cell_content))
        table.append(row)
    data = {
        "title": rubric.name,
        "table_data": table,
    }
    return render(request, 'rubrica/modify.html', context=data)
