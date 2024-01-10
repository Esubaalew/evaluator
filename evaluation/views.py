from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views import View

from evaluation.forms import EmployeeRegistrationForm, EvaluationForm
from evaluation.models import Employee, CustomUser


class CustomLoginView(LoginView):
    template_name = 'evaluation/auth/login.html'

    class CustomLoginView(LoginView):
        template_name = 'evaluation/auth/login.html'

        def get_success_url(self):
            if self.request.user.is_staff:
                return reverse('admin:index')
            else:
                return reverse('evaluation:dashboard')


@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to access the dashboard.')
        return redirect('evaluation:login')
    if request.user.is_staff:
        return render(request, 'evaluation/admin/warn.html')
    return render(request, 'evaluation/employee/dashboard.html', )


@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('evaluation:login')
    if request.user.is_staff:
        return render(request, 'evaluation/admin/warn.html')
    else:
        return render(request, 'evaluation/employee/profile.html', )


def index(request):
    return render(request, 'evaluation/employee/index.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('evaluation:index')


def employee_registration(request):
    if not request.user.is_staff:
        return render(request, 'evaluation/employee/warn.html')
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('evaluation:login'))
    else:
        form = EmployeeRegistrationForm()

    return render(
        request,
        'evaluation/auth/register.html',
        {'form': form}
    )


class EvaluationCreateView(View):
    template_name = 'evaluation/employee/evaluate.html'

    def get(self, request, *args, **kwargs):

        initial_data = {'source': request.user.username, 'evaluatee': request.user.username}

        # Pass the initial data to the form
        form = EvaluationForm(initial=initial_data)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Process the submitted form
        form = EvaluationForm(request.POST)

        if form.is_valid():
            # Save the evaluation
            evaluation = form.save(commit=False)
            evaluation.evaluator = request.user
            evaluation.save()

            return redirect('evaluation:evaluate')
        else:
            # Form is not valid, re-render the form with errors
            return render(request, self.template_name, {'form': form})
