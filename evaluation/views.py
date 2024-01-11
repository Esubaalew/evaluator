from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from evaluation.forms import EmployeeRegistrationForm, EvaluationForm
from evaluation.models import Employee, CustomUser, Evaluation


class CustomLoginView(LoginView):
    template_name = 'evaluation/auth/login.html'

    def get_success_url(self):
        return reverse('evaluation:index')


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

    else:
        return render(request, 'evaluation/employee/profile.html', )


def index(request):
    return render(request, 'evaluation/employee/index.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('evaluation:index')


class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = 'evaluation/admin/creation.html'
    context_object_name = 'user'


def employee_registration(request):
    if not request.user.is_staff:
        return render(request, 'evaluation/employee/warn.html')
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('evaluation:user_detail', pk=user.pk)
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
        form = EvaluationForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = EvaluationForm(request.POST)

        if form.is_valid():
            # Convert form data to Decimal instances
            question1 = Decimal(request.POST.get('question1'))
            question2 = Decimal(request.POST.get('question2'))
            question3 = Decimal(request.POST.get('question3'))
            question4 = Decimal(request.POST.get('question4'))
            question5 = Decimal(request.POST.get('question5'))
            question6 = Decimal(request.POST.get('question6'))
            question7 = Decimal(request.POST.get('question7'))
            question8 = Decimal(request.POST.get('question8'))

            # Save the evaluation
            evaluation = form.save(commit=False)
            evaluation.evaluator = request.user
            evaluation.question1 = question1
            evaluation.question2 = question2
            evaluation.question3 = question3
            evaluation.question4 = question4
            evaluation.question5 = question5
            evaluation.question6 = question6
            evaluation.question7 = question7
            evaluation.question8 = question8
            evaluation.evaluator = request.user
            evaluation.save()

            return redirect('evaluation:evaluation_detail', pk=evaluation.pk)
        else:
            return render(request, self.template_name, {'form': form})


class EvaluationDetailView(DetailView):
    model = Evaluation
    template_name = 'evaluation/evaluation/detail.html'  # Specify your template path
    context_object_name = 'evaluation'  # Use this variable name in your template


@method_decorator(login_required, name='dispatch')
class UserEvaluationsView(ListView):
    model = Evaluation
    template_name = 'evaluation/employee/evaluations.html'
    context_object_name = 'evaluations'

    def get_queryset(self):
        # Filter evaluations for the logged-in user
        return Evaluation.objects.filter(evaluator=self.request.user).order_by('-date_evaluated')


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)

    return render(
        request,
        'evaluation/admin/creation.html',
        {'employee': employee}
    )
