# # users/forms.py
from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import EvaluatorUser


class EvaluatorUserCreationForm(forms.ModelForm):

    class Meta(forms.ModelForm):
        model = EvaluatorUser
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(EvaluatorUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False


class EvaluatorUserRemoveForm(forms.Form):
    id = forms.IntegerField()


# class EvaluatorUserChangeForm(UserChangeForm):
#
#     class Meta:
#         model = EvaluatorUser
#         fields = ('first_name', 'last_name', 'email')
#
#     def __init__(self, *args, **kwargs):
#         super(EvaluatorUserChangeForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].required = False
#         self.fields['last_name'].required = False
