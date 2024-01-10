from django.contrib import admin

from evaluation.models import Employee, Address, Evaluation


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('evaluator', 'source', 'date_evaluated', 'evaluatee')
