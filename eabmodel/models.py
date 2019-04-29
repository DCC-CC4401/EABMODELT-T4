from django.db import models
# Create your models here.

#
# class Admin(models.Model):
#     pass
#


class Evaluator(models.Model):
    pass


class Course(models.Model):

    code = models.CharField(max_length=7)
    name = models.CharField(max_length=255)
    section = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    SEMESTER_CHOICES = (
        ('O', 'Otoño'),
        ('P', 'Primavera'),
        ('V', 'Verano'),
    )

    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)

    class Meta:
        unique_together = ["code", "section", "year", "semester"]


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # run = models.IntegerField() # es necesario?
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        unique_together = ["first_name", "last_name", "course"]


class Team(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    active = models.BooleanField()

    class Meta:
        unique_together = ["name", "course"]


class StudentAtTeam(models.Model):

    join_date = models.DateTimeField(auto_now_add=True)
    left_date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
