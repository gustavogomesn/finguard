from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    created_at = models.DateField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=50)
    value = models.FloatField()
    installments = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return (f'Expense: {self.name} - {self.value} - {self.installments}')

class FixedExpense(models.Model):
    created_at = models.DateField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=50)
    value = models.FloatField()
    end_month = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return (f'Fixed Expense: {self.name} - {self.value}')
    
class Income(models.Model):
    created_at = models.DateField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=50)
    value = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return (f'Income: {self.name} - {self.value}')
    
class FixedIncome(models.Model):
    created_at = models.DateField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=50)
    value = models.FloatField()
    end_month = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return (f'Fixed Income: {self.name} - {self.value}')
