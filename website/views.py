from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import SignUpForm, AddExpenseForm, AddFixedExpenseForm, AddIncomeForm, AddFixedIncomeForm
from .models import Expense, FixedExpense, Income, FixedIncome
from .utils import get_expenses_summary, get_incomes_summary, get_expense_category_data
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

def login_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials')
            return redirect('home')
        else: 
            login(request, user)
            return redirect('home')

    else: 
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            messages.success(request, "You register successfully!")
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    return render(request, 'signup.html', {'form': form})


@login_required
def home(request, year = date.today().year, month = date.today().month):
    current_date = date(year, month, 1)
    
    expenses_data = get_expenses_summary(request, current_date, expenses = Expense, fixed_expenses = FixedExpense)
    incomes_data = get_incomes_summary(request, current_date, incomes = Income, fixed_incomes = FixedIncome)
    expenses_by_category = get_expense_category_data(request, current_date, expenses = Expense, fixed_expenses = FixedExpense)
    
    add_expense_form = AddExpenseForm()
    add_income_form = AddIncomeForm()
    
    previous_year = (current_date - relativedelta(months=1)).year
    previous_month = (current_date - relativedelta(months=1)).month
    next_year = (current_date + relativedelta(months=1)).year
    next_month = (current_date + relativedelta(months=1)).month
    
    additional_data = {
        **expenses_data,
        **incomes_data,
        **expenses_by_category,
        'balance': round(incomes_data['incomes_values'][1] - expenses_data['values'][1], 2),
        'current_year': current_date.year,
        'current_month': current_date.month,
        "current_text_month": calendar.month_name[month],
        'previous_year': previous_year,
        'previous_month': previous_month,
        'next_year': next_year,
        'next_month': next_month,
        "add_expense_form": add_expense_form,
        "add_income_form": add_income_form
        }
    return render(request, 'home.html', additional_data)

@login_required
def transactions(request, year, month):
    current_date = date(year=year, month=month, day=1)
    
    last_day = calendar.monthrange(year, month)[1]
    date_verification = Q(created_at__lte = date(year, month, last_day))
    fixed_incomes = FixedIncome.objects.filter(date_verification, Q(end_month__isnull = True) | Q(end_month__gte = current_date), user_id = request.user.id)
    for fi in fixed_incomes:
        fi.is_income = True
        fi.is_fixed = True
    filter_transations = list(fixed_incomes).copy()
    
    incomes = Income.objects.filter(user_id = request.user.id).order_by('-created_at')
    for i in incomes:
        i.is_income = True
        if i.created_at.year == year and i.created_at.month == month:
            filter_transations.append(i)
    
    fixed_expenses = FixedExpense.objects.filter(date_verification , Q(end_month__isnull = True) | Q(end_month__gte = current_date), user_id = request.user.id)
    for fe in fixed_expenses:
        fe.is_fixed = True
    filter_transations += list(fixed_expenses)
    
    expenses = Expense.objects.filter(user_id = request.user.id).order_by('created_at')
    
    for expense in expenses:
        expense.is_fixed = False
        expense.created_at_aux = expense.created_at.replace(day=1)
        if expense.installments > 1 and (expense.created_at_aux <= current_date < expense.created_at_aux + relativedelta(months=expense.installments)):
            diff = relativedelta(current_date, expense.created_at_aux)
            diff_days = ((diff.years)*12)*30 + diff.months*30 + diff.days
            expense.current_installment = round(diff_days/30) + 1
            filter_transations.append(expense)
        elif expense.created_at_aux.year == year and expense.created_at_aux.month == month:
            filter_transations.append(expense)
            
    previous_year = (current_date - relativedelta(months=1)).year
    previous_month = (current_date - relativedelta(months=1)).month
    next_year = (current_date + relativedelta(months=1)).year
    next_month = (current_date + relativedelta(months=1)).month
    
    
    add_expense_form = AddExpenseForm()
    add_income_form = AddIncomeForm()
    return render(request, 'transactions.html', {
        "current_text_month": calendar.month_name[month],
        'current_year': current_date.year,
        'current_month': current_date.month,
        'previous_year': previous_year,
        'previous_month': previous_month,
        'next_year': next_year,
        'next_month': next_month,
        "transactions": filter_transations,
        "add_expense_form": add_expense_form,
        "add_income_form": add_income_form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user_id = request.user.id
            if expense.installments > 1:
                expense.value = round(expense.value / expense.installments, 2)
            expense.save()
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('home')
    

@login_required
def add_fixed_expense(request):
    if request.method == 'POST':
        cleaned_data = {
            "created_at": request.POST.dict()['created_at'],
            "name": request.POST.dict()['name'],
            "description" : request.POST.dict()['description'],
            "category": request.POST.dict()['category'],
            "value": request.POST.dict()['value'],
            "end_month": None
        }
        form = AddFixedExpenseForm(cleaned_data)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user_id = request.user.id
            expense.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('home')

@login_required
def edit_expense(request, type, id):
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            if type == 'fixed':
                expense = FixedExpense.objects.filter(id=id, user_id=request.user.id)
                expense.delete()
            else:
                expense = Expense.objects.filter(id=id, user_id=request.user.id)
                expense.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        if type == 'fixed':
            cleaned_data = {
            "created_at": request.POST.dict()['date'],
            "name": request.POST.dict()['name'],
            "description" : request.POST.dict()['description'],
            "category": request.POST.dict()['category'],
            "value": request.POST.dict()['value'],
            "end_month": request.POST.dict()['end-month']
            }
            if(not cleaned_data['end_month']):
                cleaned_data.pop('end_month')
            expense = FixedExpense.objects.filter(id=id, user_id=request.user.id)
            expense.update(**cleaned_data)
        else:
            cleaned_data = {
                "created_at": request.POST.dict()['date'],
                "category": request.POST.dict()['category'],
                "name": request.POST.dict()['name'],
                "description" : request.POST.dict()['description'],
                "value": float(request.POST.dict()['value'])/float(request.POST.dict()['installments']),
                "installments": request.POST.dict()['installments'],
            }
            expense = Expense.objects.filter(id=id, user_id=request.user.id)
            expense.update(**cleaned_data)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return redirect('home')
    
@login_required
def add_income(request):
    if request.method == 'POST' :
        form = AddIncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user_id = request.user.id
            income.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('home')
    

@login_required
def add_fixed_income(request):
    if request.method == 'POST' :
        cleaned_data = {
            "created_at": request.POST.dict()['created_at'],
            "name": request.POST.dict()['name'],
            "description" : request.POST.dict()['description'],
            "category": request.POST.dict()['category'],
            "value": request.POST.dict()['value'],
            "end_month": None
        }
        form = AddFixedIncomeForm(cleaned_data)
        if form.is_valid():
            income = form.save(commit=False)
            income.user_id = request.user.id
            income.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('home')
    
@login_required
def edit_income(request, type, id):
    if request.method == 'POST' :
        if request.POST.get('_method') == 'DELETE':
            if type == 'fixed':
                income = FixedIncome.objects.filter(id=id, user_id=request.user.id)
                income.delete()
            else:
                income = Income.objects.filter(id=id, user_id=request.user.id)
                income.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        if type == 'fixed':
            cleaned_data = {
            "created_at": request.POST.dict()['date'],
            "name": request.POST.dict()['name'],
            "description" : request.POST.dict()['description'],
            "category": request.POST.dict()['category'],
            "value": request.POST.dict()['value'],
            "end_month": request.POST.dict()['end-month']
            }
            if(not cleaned_data['end_month']):
                cleaned_data.pop('end_month')
            income = FixedIncome.objects.filter(id=id, user_id=request.user.id)
            income.update(**cleaned_data)
        else:
            cleaned_data = {
                "created_at": request.POST.dict()['date'],
                "category": request.POST.dict()['category'],
                "name": request.POST.dict()['name'],
                "description" : request.POST.dict()['description'],
                "value": request.POST.dict()['value']
            }
            income = Income.objects.filter(id=id, user_id=request.user.id)
            income.update(**cleaned_data)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return redirect('home')