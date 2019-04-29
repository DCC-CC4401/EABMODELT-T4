from django.db import models

# Create your models here.


class Rubric(models.Model):
    name = models.CharField(max_length=255)

    suggested_presentation_time = models.TimeField()

    n_compliance_lvl = models.PositiveSmallIntegerField()
    n_evaluated_aspect = models.PositiveSmallIntegerField()
    rubric = models.TextField()
    completed = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #rubrica
