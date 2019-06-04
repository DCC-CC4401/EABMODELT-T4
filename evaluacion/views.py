from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test

from evaluacion.forms import EvaluationForm, AddEvaluatorForm, AddEvaluatorForm2
from evaluacion.models import *
from eabmodel.models import *
from users.models import *
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
import json


@login_required
def index(request, extra_context={}):

    if(request.user.is_admin):
        # pass
        evaluations = Evaluation.objects.all()
    else:
        evaluations = Evaluation.objects.all().filter(evaluators=request.user)

    context = {'evaluations': evaluations, 'form': EvaluationForm(prefix="agregar")}
    context.update(extra_context)
    return render(request, 'evaluacion/index.html', context)

@login_required
def view_evaluation(request, id):
    evaluation = get_object_or_404(Evaluation, id=id)
    context = {'evaluation': evaluation}
    return render(request, 'evaluacion/verEval.html', context)

@login_required
def edit_evaluation(request, id):
    evaluation = get_object_or_404(Evaluation, id=id)
    context = {'evaluation': evaluation}
    return render(request, 'evaluacion/verEval.html', context)

def rm_evaluation(reques, id):
    ev = get_object_or_404(Evaluation, id=id)
    ev.delete()
    return redirect(reverse("evaluacion:index"))


@login_required
def add_evaluation(request):
    extra_context = {}


    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    if request.method != 'POST':
        form = EvaluationForm(prefix="agregar")

    else:
        form = EvaluationForm(request.POST, prefix="agregar")
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    # form
    extra_context.update({'form': form})
    response = index(request, extra_context)
    return response



@csrf_exempt
def openEval(request, name, course, section, semester, year, team):

    semester_name = getSemester(semester)
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string, encoding='utf-8')
        gdet = json.loads(data['grade_detail'], encoding='utf-8')
        course_obj = get_object_or_404(Course, code=course, section=section, year=year, semester=semester_name)
        evaluation = get_object_or_404(Evaluation, name=name, course=course_obj)
        team_evaluated = get_object_or_404(Team, id=team)
        evaluator = get_object_or_404(EvaluatorUser, id=1)
        teamEval = get_object_or_404(TeamEvaluation, team=team_evaluated, evaluation=evaluation)
        gDetail = dict()
        grade = 1
        for ac in gdet:
            gDetail[ac[0]] = ac[2]
            grade += ac[2]
        TeamEvaluationGrade.objects.create(submitted_at=data['submitted_at'],
                                           updated_at=data['updated_at'],
                                           team_evaluation=teamEval,
                                           evaluator=evaluator,
                                           grade_detail=json.dumps(gDetail),
                                           final_grade=grade)
        return JsonResponse(gDetail)
    else:
        curso = get_object_or_404(Course, code=course, section=section, semester=semester_name, year=year)
        equipo = get_object_or_404(Team, id=team, course=curso.id)
        evalActual = get_object_or_404(Evaluation, name=name, course=curso)
        if not TeamEvaluation.objects.filter(team=equipo, evaluation=evalActual).exists():
            return HttpResponseBadRequest("<div style='text-align:center'>La evaluación para este equipo aún no está "
                                          + "disponible. Por favor espere"
                                          + " hasta que el/la profesor/a comience esta evaluación.</div>"
                                          + "<div style='text-align:center'><a href=http://localhost:8000/evaluacion>"
                                          + "Volver al Menú de Evaluaciones</a></div>")
        if request.user not in evalActual.evaluators.all():
            return HttpResponseForbidden("<div style='text-align:center'>Usted no está asignado para esta evaluación. "
                                         + "Si cree que esto es un error comuníquese con el/la profesor/a "
                                         + "a cargo.</div>"
                                         + "<div style='text-align:center'><a href=http://localhost:8000/evaluacion>"
                                         + "Volver al Menú de Evaluaciones</a></div>")
        try:
            parsedRub = json.loads(evalActual.rubric.rubric)
        except(ValueError, KeyError, TypeError):
            print("Error en Formato de Rúbrica")
            return HttpResponseBadRequest("Error en Formato de Rúbrica")
        rubrica = getRubrica2(parsedRub["rubric"])
        context = dict()
        context['team'] = equipo.name
        context['stage'] = evalActual.name
        context['course'] = course
        context['section'] = section
        context['year'] = year
        context['rubric'] = rubrica
        context['numberOfAspects'] = len(rubrica)
        context['team_id'] = team
        context['semester'] = semester_name
        context['semester_code'] = semester
        return render(request, 'evaluacion/evaluacion.html', context=context)

@csrf_exempt
def openEvalAdmin(request, name, course, section, semester, year, team):

    semester_name = getSemester(semester)


    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string, encoding='utf-8')
        gdet = json.loads(data['grade_detail'], encoding='utf-8')
        presenters = json.loads(data['presenters'], encoding='utf-8')
        course_obj = get_object_or_404(Course, code=course, section=section, year=year, semester=semester_name)
        evaluation = get_object_or_404(Evaluation, name=name, course=course_obj)
        team_evaluated = get_object_or_404(Team, id=team)
        teamEval = get_object_or_404(TeamEvaluation, team=team_evaluated, evaluation=evaluation)
        for pres in presenters:
            teamEval.presenter.add(Student.objects.get(id=pres[1]))
        gDetail = dict()
        grade = 1
        for ac in gdet:
            gDetail[ac[0]] = ac[2]
            grade += ac[2]
        discs = encodeDiscount(evaluation.rubric.max_presentation_time, evaluation.rubric.min_presentation_time,
                               getSeconds(data['time']))
        gDetail['Time'] = discs[0]
        gDetail['Type'] = discs[1]
        TeamEvaluationGrade.objects.create(submitted_at=data['submitted_at'],
                                           updated_at=data['updated_at'],
                                           team_evaluation=teamEval,
                                           evaluator=request.user,
                                           grade_detail=json.dumps(gDetail),
                                           final_grade=grade)
        return JsonResponse(gDetail)

    else:

        curso = get_object_or_404(Course, code=course, section=section, semester=semester_name, year=year)
        equipo = get_object_or_404(Team, id=team, course_id=curso.id)
        evalActual = get_object_or_404(Evaluation, name=name, course=curso)
        if not TeamEvaluation.objects.filter(team=equipo, evaluation=evalActual).exists():
            return HttpResponseBadRequest("<div style='text-align:center'> La evaluación para este equipo aún no está"
                                          + " disponible. Puede comenzarla en el"
                                          + " <a href=http://localhost:8000/evaluacion/>menú de evaluaciones</a> si lo"
                                          + " desea.</div>")
        try:
            parsedRub = json.loads(evalActual.rubric.rubric)
            print(parsedRub['rubric'])
        except(ValueError, KeyError, TypeError):
            print("Error en Formato de Rúbrica")
            return HttpResponseBadRequest("Error en Formato de Rúbrica")

        rubrica = getRubrica2(parsedRub['rubric'])
        alreadyPresented = []
        presenting_group = []

        for ev in TeamEvaluation.objects.filter(team=equipo):
            for alumn in ev.presenter.all():
                name = alumn.first_name + " " + alumn.last_name
                alreadyPresented.append(name)
        for a in StudentAtTeam.objects.filter(team=equipo.id, active=True):
            student_name = a.student.first_name + " " + a.student.last_name
            if student_name in alreadyPresented:
                pres = True
            else:
                pres = False
            presenting_group.append([student_name, pres, a.student.id])
        context = dict()
        context['group'] = presenting_group
        context['team'] = equipo.name
        context['team_id'] = team
        context['course'] = course
        context['section'] = section
        context['semester_code'] = semester
        context['year'] = year
        context['semester'] = semester_name
        context['stage'] = evalActual.name
        context['evaluation'] = evalActual
        context['rubric'] = rubrica
        context['evaluators'] = [["Jocelyn Simmonds", False], ["Pablo Miranda", True]]
        return render(request, 'evaluacion/evaluacionadmin.html', context=context)


def openEvalAdmin2(request, id):
    a = Evaluation.objects.get(pk=id)
    name = a.name

    print(a.course)
    course = a.course.code
    section = a.course.section
    semester = a.course.semester
    year = a.course.year
    team = 1
    return openEvalAdmin(request, name, course, section, semester[0], year, team)

@login_required
def postEval(request, name, course, section, semester, year, team):
    semester_name = getSemester(semester)
    actualCourse = get_object_or_404(Course, code=course, section=section, year=year, semester=semester_name)
    evaluation = get_object_or_404(Evaluation, name=name, course=actualCourse)
    teamEvaluated = get_object_or_404(Team, id=team)
    teamEvaluation = get_object_or_404(TeamEvaluation, team=teamEvaluated, evaluation=evaluation)
    evaluator = get_object_or_404(EvaluatorUser, id=1)
    gradeByEval = get_object_or_404(TeamEvaluationGrade, team_evaluation=teamEvaluation, evaluator=evaluator)
    parsedRub = getRubrica2(json.loads(evaluation.rubric.rubric)["rubric"])
    accomplishment = getAccomplishment(json.loads(gradeByEval.grade_detail), parsedRub)
    return render(request, 'evaluacion/postevaluacion.html', context={"scores": accomplishment,
                                                                      "stage": name,
                                                                      "course": course,
                                                                      "section": section,
                                                                      "semester": semester_name,
                                                                      "year": year,
                                                                      "team": teamEvaluated.name})

@csrf_exempt
@login_required
def postEvalAdmin(request, name, course, section, semester, year, team):
    semester_name = getSemester(semester)
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string, encoding='utf-8')
        course_obj = get_object_or_404(Course, code=course, section=section, year=year, semester=semester_name)
        evaluation = get_object_or_404(Evaluation, name=name, course=course_obj)
        team = get_object_or_404(Team, id=data['team'])
        TeamEvaluation.objects.create(team=team,
                                      evaluation=evaluation,
                                      duration=0,
                                      is_active=True)
        return JsonResponse(data)
    else:
        actualCourse = get_object_or_404(Course, code=course, section=section, year=year, semester=semester_name)
        evaluation = get_object_or_404(Evaluation, name=name, course=actualCourse)
        teamEvaluated = get_object_or_404(Team, id=team)
        teamEvaluation = get_object_or_404(TeamEvaluation, team=teamEvaluated, evaluation=evaluation)
        evaluator = get_object_or_404(EvaluatorUser, id=1)
        gradeByEval = get_object_or_404(TeamEvaluationGrade, team_evaluation=teamEvaluation, evaluator=evaluator)
        parsedRub = getRubrica2(json.loads(evaluation.rubric.rubric)["rubric"])
        detail = json.loads(gradeByEval.grade_detail)
        accomplishment = getAccomplishment(detail, parsedRub)
        courseTeams = Team.objects.filter(course=actualCourse, active=True)
        pendingTeams = getTeams(TeamEvaluation.objects.filter(evaluation=evaluation), courseTeams)
        discount = getDiscount(detail)
        return render(request, 'evaluacion/postevaluacionadmin.html', context={"scores": accomplishment,
                                                                               "stage": name,
                                                                               "course": course,
                                                                               "section": section,
                                                                               "semester": semester_name,
                                                                               "semester_code": semester,
                                                                               "team_id": team,
                                                                               "year": year,
                                                                               "team": teamEvaluated.name,
                                                                               "left_teams": pendingTeams,
                                                                               "time_discount": discount[0],
                                                                               "less_time": discount[1],
                                                                               "infraction": discount[2],
                                                                               "infraction2": discount[3]})

def getRubrica(eval):
    try:
        parsedRub = json.loads(eval.rubric.rubric)
    except(ValueError, KeyError, TypeError):
        print("Error en Formato de Rúbrica")
        return HttpResponseBadRequest("Error en Formato de Rúbrica")
    rubrica = []
    i = 0
    for a in parsedRub:
        i += 1
        pointsList = []
        for points, text in a.items():
            if points == 'Aspecto':
                pass
            else:
                pointsList.append([float(points), text])
        rubrica.append([i, a['Aspecto'], pointsList])
    return rubrica


def getAccomplishment(scores, rub):
    accList = []
    for item in rub:
        points = scores[str(item[0])]
        aspect = item[1]
        max = float(item[2][-1][0])
        accompl = 100*(points/max)
        accompl = int(round(accompl, 0))
        accList.append([aspect, accompl])
    return accList


def getSemester(sem):
    if sem == 'O':
        return "Otoño"
    elif sem == 'P':
        return "Primavera"
    else:
        return "Verano"


def getTeams(evaltms, alltms):
    evalteams = []
    leftteams = []
    for item in evaltms:
        evalteams.append(item.team)
    for team in alltms:
        # if team in evalteams:
            # pass
        # else:
        leftteams.append([team.name, team.id])
    return leftteams


def getDiscount(det):
    if det['Time'] != "OK":
        if det['Type'] == "Menor":
            return [True, det['Time'], "menos", "mínimo"]
        else:
            return [True, det['Time'], "más", "máximo"]
    else:
        return [False, 0, 0, 0]


def getSeconds(time):
    time2 = time.split(":")
    mins = int(time2[0])
    secs = int(time2[1])
    return mins*60 + secs


def encodeDiscount(max,min,time):
    if time < min:
        return [min-time, "Menor"]
    elif time > max:
        return [time-max, "Mayor"]
    else:
        return ["OK", "OK"]


def getRubrica2(rub):
    levels = rub[0]
    rubric = []
    i = 0
    for asp in rub:
        if i == 0:
            pass
        else:
            pointsList = []
            j = 0
            while j < len(asp):
                if j == 0:
                    pass
                else:
                    pointsList.append([float(levels[j]), asp[j]])
                j += 1
            rubric.append([i, asp[0], pointsList])
        i += 1
    return rubric

def teamevaluation_detail_view(request, teameval_id):
    #obj = TeamEvaluation.objects.get(id=eval_id)
    obj = get_object_or_404(TeamEvaluation, id=teameval_id)
    evaluators_list = EvaluatorUser.objects.all() #queryset, list of evaluator users
    rubrics = Rubric.objects.all() #queryset, list of all rubrics
    context = {
      'teamevaluation' : obj,
      'evaluation' : obj.evaluation,
      'evaluators' : obj.evaluation.evaluators,
      'evaluators-list': evaluator_list,
      'rubrics':rubrics
    }
    return render(request, 'evaluacion/addevaluator.html', context)

def add_evaluator_view(request, id):
    evaluation = get_object_or_404(Evaluation, id=id)
    print(evaluation)
    print(evaluation.evaluators.all())

    #obj = TeamEvaluation.objects.filter(evaluation=evaluation)
    #evaluators_to_exclude = []
    #if TeamEvaluationGrade.DoesNotExist == False:
        #teamevaluationgrades = TeamEvaluationGrade.objects.filter(team_evaluation=obj)
        #evaluators_to_exclude = [ grade.evaluator for grade in teamevaluationgrades ]
    #qs = obj.evaluation.evaluators.remove(*evaluators_to_exclude)
    evaluators_list = EvaluatorUser.objects.all() #queryset, list of evaluator users
    rubrics = Rubric.objects.all() #queryset, list of all rubrics

    form = AddEvaluatorForm(request.POST or None)
    actualCourse = get_object_or_404(Course, code=evaluation.course.code)
    courseTeams = Team.objects.filter(course=actualCourse, active=True)
    pendingTeams = getTeams(TeamEvaluation.objects.filter(evaluation=evaluation), courseTeams)
    if form.is_valid():
        for i in form.cleaned_data["evaluators"].all():
            evaluation.evaluators.add(i)
        evaluation.save()

    else:
        pass

    context = {
        'evaluation': evaluation,
        'evaluators': evaluation.evaluators.all(),
        'all_evaluator': EvaluatorUser.objects.all(),
        'evaluators-list': evaluators_list,
        'left_teams': pendingTeams,
        'rubrics': rubrics,
        'form': form,
        'editar_form': EvaluationForm(instance=evaluation),
    }
    return render(request, 'evaluacion/addevaluator.html', context)

@csrf_exempt
def open_evaluation(request, id):
    if request.method == "POST":
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string, encoding='utf-8')
        if data['func'] == "openEval":
            eval = get_object_or_404(Evaluation, id=data['id'])
            eval.is_active = True
            eval.save()
        return HttpResponse(True)

    else:
        evaluation = get_object_or_404(Evaluation, id=id)
        team = get_object_or_404(Team, id=data['team'])
        TeamEvaluation.objects.create(team=team,
                                      evaluation=evaluation,
                                      duration=0,
                                      is_active=True)
        return JsonResponse(data)

def rm_evaluator(request, eva_id, ev_id):
    evaluation = get_object_or_404(Evaluation, id=eva_id)
    evaluation.evaluators.remove(EvaluatorUser.objects.get(pk=ev_id))
    return redirect('/evaluacion/' + str(eva_id) + '/addEvaluator/')


def add_evaluator(request):
    extra_context = {}
    response = {'result': 'false'}
    if not request.user.is_admin:
        return HttpResponseNotFound('Sorry')

    if request.method != 'POST':
        form = AddEvaluatorForm2(prefix="agregar")

    else:
        form = AddEvaluatorForm2(request.POST, prefix="agregar")
        if form.is_valid():
            evaluation = Evaluation.objects.get(pk=form.cleaned_data['evaluation_id'])
            evaluation.evaluators.add(EvaluatorUser.objects.get(pk=form.cleaned_data['evaluator_id']))
            evaluation.save()
            response = {'result': 'success'}

    return HttpResponse(json.dumps(response), content_type="application/json")





def edit_rubric(request, id): 
    instance = get_object_or_404(Evaluation, id=id)
    form = EditRubricForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/evaluacion/'+str(id)+'/addEvaluator/')
    context = {
        'evaluation': instance,
        'form': form
      }
    return render(request, 'evaluacion/editrubric.html', context) 

def edit_dates(request,id):
    instance = get_object_or_404(Evaluation, id=id)
    form = EditDatesForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/evaluacion/'+str(id)+'/addEvaluator/')
    context = {
        'evaluation': instance,
        'form': form
      }
    return render(request, 'evaluacion/editdates.html', context) 


