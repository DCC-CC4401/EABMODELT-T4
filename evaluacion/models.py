from django.db import models

from eabmodel.models import Student, Course, Team, Evaluator
from rubrica.models import Rubric

# Create your models here.


class Evaluation(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete = models.PROTECT)

    rubric = models.ForeignKey(Rubric, on_delete = models.PROTECT)
    presentation_time = models.TimeField()

    evaluators = models.ManyToManyField(Evaluator)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ["name", "date", ]


class TeamEvaluation(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, models.PROTECT)
    presenter = models.ManyToManyField(Student)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)


class TeamEvaluationGrade(models.Model):

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    team_evaluation = models.ForeignKey(TeamEvaluation, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Evaluator, on_delete=models.PROTECT)
    grade_detail = models.TextField()
    final_grade = models.FloatField()
    comment = models.TextField()
