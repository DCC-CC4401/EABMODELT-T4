from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Course(models.Model):
    code = models.CharField('código', max_length=7, help_text=_('código del curso'))
    name = models.CharField('nombre', max_length=150, help_text=_('nombre del curso'))
    section = models.PositiveSmallIntegerField('sección', default=1, help_text=_('sección del curso'))
    year = models.PositiveSmallIntegerField('año', default=2019, help_text=_('año que se dicta el curso'))

    SEMESTER_CHOICES = (
        ('Otoño', 'Otoño'),
        ('Primavera', 'Primavera'),
        ('Verano', 'Verano'),
    )
    semester = models.CharField(max_length=9, choices=SEMESTER_CHOICES, default='Otoño', help_text=_('semestre que se dicta el curso'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["code", "section", "year", "semester"]
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'

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