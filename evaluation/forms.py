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
        fields = ['evaluatee', 'source']

    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)

        self.questions = [
            ('question1', 'ፍትሐዊ አገልግሎት መስጠት', 5),
            ('question2', 'ትነሽነት', 5),
            ('question3', 'ሚዛናዊነት', 5),
            ('question4', 'ውሳኔ ሰጭነት', 5),
            ('question5', 'ተገልጋቶችን መረዳት', 5),
            ('question6', 'ስነ ምግባሩ', 5),
            ('question7', 'ስራን በጥራት የመስራት', 5),
            ('question8', 'የስራ ትጋት', 5),
        ]

        for field_name, question_text, max_value in self.questions:
            self.fields[field_name] = forms.IntegerField(
                label=question_text,
                widget=forms.NumberInput(attrs={'min': 1, 'max': max_value}),
                help_text=f"(Max points: {max_value})"
            )
