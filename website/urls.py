from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register-user/', views.register_user, name='register'),
    path('transactions/<int:year>/<int:month>', views.transactions, name='transactions'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('add-fixed-expense/', views.add_fixed_expense, name='add-fixed-expense'),
    path('edit-expense/<type>/<int:id>', views.edit_expense, name='edit-expense'),
    path('add-income/', views.add_income, name='add-income'),
    path('add-fixed-income/', views.add_fixed_income, name='add-fixed-income'),
    path('edit-income/<type>/<int:id>', views.edit_income, name='edit-income'),
]
