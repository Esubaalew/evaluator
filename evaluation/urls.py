from django.urls import path
from . import views
from .views import EvaluationCreateView, EvaluationDetailView, UserEvaluationsView, CustomUserDetailView

app_name = 'evaluation'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'registration/',
        views.employee_registration,
        name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('evaluate/', EvaluationCreateView.as_view(), name='evaluate'),
    path('evaluation/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('evaluations/', UserEvaluationsView.as_view(), name='evaluations'),
    path('user/<int:pk>/', CustomUserDetailView.as_view(), name='user_detail'),
]
