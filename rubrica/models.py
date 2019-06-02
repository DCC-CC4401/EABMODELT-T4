from django.db import models


class Rubric(models.Model):
    name = models.CharField(max_length=255)
    min_presentation_time = models.PositiveSmallIntegerField()  # en segundos
    max_presentation_time = models.PositiveSmallIntegerField()  # en segundos
    n_compliance_lvl = models.PositiveSmallIntegerField()
    n_evaluated_aspect = models.PositiveSmallIntegerField()
    rubric = models.TextField()
    completed = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

