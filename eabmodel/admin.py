from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Evaluator)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Team)
admin.site.register(StudentAtTeam)