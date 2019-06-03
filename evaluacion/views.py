from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from evaluacion.models import *
from eabmodel.models import *
from users.models import *
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
import json


@login_required
def index(request):
    return render(request, 'evaluacion/index.html', context={})

@csrf_exempt
@login_required
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
        rubrica = getRubrica2(parsedRub)
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
@user_passes_test(lambda u: u.is_superuser)
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
        equipo = get_object_or_404(Team, id=team, course=curso.id)
        evalActual = get_object_or_404(Evaluation, name=name, course=curso)
        if not TeamEvaluation.objects.filter(team=equipo, evaluation=evalActual).exists():
            return HttpResponseBadRequest("<div style='text-align:center'> La evaluación para este equipo aún no está"
                                          + " disponible. Puede comenzarla en el"
                                          + " <a href=http://localhost:8000/evaluacion/>menú de evaluaciones</a> si lo"
                                          + " desea.</div>")
        try:
            parsedRub = json.loads(evalActual.rubric.rubric)
        except(ValueError, KeyError, TypeError):
            print("Error en Formato de Rúbrica")
            return HttpResponseBadRequest("Error en Formato de Rúbrica")
        rubrica = getRubrica2(parsedRub)
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
        context['rubric'] = rubrica
        context['evaluators'] = [["Jocelyn Simmonds", False], ["Pablo Miranda", True]]
        return render(request, 'evaluacion/evaluacionadmin.html', context=context)


@login_required
def postEval(request, name, course, section, semester, year, team):
    semester_name = getSemester(semester)
    actualCourse = get_object_or_404(Course, code=course, section=section, year=year, semester=semester_name)
    evaluation = get_object_or_404(Evaluation, name=name, course=actualCourse)
    teamEvaluated = get_object_or_404(Team, id=team)
    teamEvaluation = get_object_or_404(TeamEvaluation, team=teamEvaluated, evaluation=evaluation)
    evaluator = get_object_or_404(EvaluatorUser, id=1)
    gradeByEval = get_object_or_404(TeamEvaluationGrade, team_evaluation=teamEvaluation, evaluator=evaluator)
    parsedRub = getRubrica2(json.loads(evaluation.rubric.rubric))
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
        parsedRub = getRubrica2(json.loads(evaluation.rubric.rubric))
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
        if team in evalteams:
            pass
        else:
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

