from django.contrib.auth.models import AbstractUser
from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        parts = [self.street, self.city, self.state, self.country]

        address_parts = filter(None, parts)
        return ', '.join(address_parts)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True)
    position = models.CharField(max_length=50, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    is_employee = models.BooleanField(default=True)
    evaluations_given = models.ManyToManyField('Evaluation', symmetrical=False,
                                               related_name='given_evaluations')
    evaluations_received = models.ManyToManyField('Evaluation', symmetrical=False,
                                                  related_name='received_evaluations')
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "All User"

    def __str__(self):
        return self.username


class Employee(CustomUser):
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


class Evaluation(models.Model):
    SOURCE_CHOICES = [
        ('self', 'Self'),
        ('boss', 'Boss'),
        ('other_employee', 'Other Employee'),
    ]

    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='evaluations_given_set')
    evaluatee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='evaluations_received_set')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    date_evaluated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation by {self.evaluator.username} for {self.evaluatee.username}"
