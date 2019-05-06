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
            print("upsi")
            raise forms.ValidationError(
               "Solo puedes crear cursos de este año o el siguiente"
            )

        return cleaned_data




