from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Evaluation)
admin.site.register(TeamEvaluation)
admin.site.register(TeamEvaluationGrade)