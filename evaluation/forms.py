# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser, Employee, Evaluation


class EmployeeRegistrationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = (
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone_number',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employee = True
        if commit:
            user.save()
        return user


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        exclude = ['evaluator', 'date_evaluated']