from django.db import models
from django.utils import timezone
# Create your models here.


class Rubric(models.Model):
    name = models.CharField(max_length=255)
    #min_presentation_time = models.DateTimeField()
    #max_presentation_time = models.DateTimeField()
    n_compliance_lvl = models.PositiveSmallIntegerField()
    n_evaluated_aspect = models.PositiveSmallIntegerField()
    rubric = models.TextField()
    completed = models.BooleanField()

    #created_at = models.DateTimeField(editable=False)
    #updated_at = models.DateTimeField()
