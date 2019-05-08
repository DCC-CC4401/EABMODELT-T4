from django import forms
from .models import Course
from datetime import datetime


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code',  'section', 'year', 'semester']

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')

        if year < datetime.now().year or year > datetime.now().year+1:
            raise forms.ValidationError(
               "Solo puedes crear cursos de este año o el siguiente"
            )
        cleaned_data['code'] = cleaned_data.get('code').upper()
        return cleaned_data


class RemoveCourseForm(forms.Form):
    id = forms.IntegerField()
