from django import forms

from .models import Evaluation
from users.models import EvaluatorUser
from rubrica.models import Rubric

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'name',
            'date',
            'final_date',
            'course',
            'rubric',
            'presentation_time',
        # 'evaluators',
        # 'is_active'
        ]
        # widgets = { }


class AddEvaluatorForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ('evaluators',)

class AddEvaluatorForm2(forms.Form):
    evaluator_id = forms.IntegerField()
    # evaluation_id = forms.IntegerField()



class EditRubricForm(forms.ModelForm):
    #rubricas = forms.ChoiceField(choices=[(rubrica.id, rubrica.rubric) for rubrica in Rubric.objects.all()])
    #rubricas = forms.ModelChoiceField(queryset=Rubric.objects.all())
    class Meta:
        model = Evaluation
        fields = ('rubric',)
        #widgets = { 'rubricas': forms.Select(attrs={'class':'select'})
        #}

class EditDatesForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
        'date',
        'final_date'
        ]