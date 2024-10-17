from django.db.models import Q
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
import calendar

from .models import Expense, FixedExpense, Income, FixedIncome

def get_expenses_summary(request):
    current_date = date.today()
    
    # Pass data from previous month to next 3 months
    months_to_graphs = []
    for rel in range(-1, 4):
        if rel == -1:
            months_to_graphs.append(current_date - relativedelta(months=1))
        else:
            months_to_graphs.append(current_date + relativedelta(months=rel))
    
    expenses = list(Expense.objects.filter(user_id = request.user.id))
    fixed_expenses = FixedExpense.objects.filter(Q(end_month__isnull = True) | Q(end_month__lte = current_date), user_id = request.user.id)
    
    next_months_sum = {
        calendar.month_name[months_to_graphs[0].month]: 0,
        calendar.month_name[months_to_graphs[1].month]: 0,
        calendar.month_name[months_to_graphs[2].month]: 0,
        calendar.month_name[months_to_graphs[3].month]: 0,
        calendar.month_name[months_to_graphs[4].month]: 0,
    }
    
    var_exp_sum = 0
    fix_exp_sum = 0
    
    for fexpense in fixed_expenses:
        fix_exp_sum += fexpense.value
        for i in range(-1, 4):
            fexpense.created_at = current_date + relativedelta(months=i)
            next_months_sum[calendar.month_name[fexpense.created_at.month]] += fexpense.value
    
    for expense in expenses:
        for month in months_to_graphs:
            if month == current_date:
                if expense.created_at.year == month.year and expense.created_at.month == month.month:
                    next_months_sum[calendar.month_name[expense.created_at.month]] += expense.value
                    var_exp_sum += expense.value
                elif expense.installments > 1 and (expense.created_at <= month < expense.created_at + relativedelta(months=expense.installments)):
                    next_months_sum[calendar.month_name[month.month]] += expense.value
                    var_exp_sum += expense.value
            else:
                if expense.created_at.year == month.year and expense.created_at.month == month.month:
                    next_months_sum[calendar.month_name[expense.created_at.month]] += expense.value
                elif expense.installments > 1 and (expense.created_at <= month < expense.created_at + relativedelta(months=expense.installments)):
                    next_months_sum[calendar.month_name[month.month]] += expense.value
    
    for key, value in next_months_sum.items():
        next_months_sum[key] = round(value, 2)
    
    return {
        "values_sum": next_months_sum.items(), 
        'months': list(next_months_sum.keys()), 
        'values': list(next_months_sum.values()),
        'var_sum': var_exp_sum,
        'fix_sum': fix_exp_sum
        }
    
def get_incomes_summary(request):
    current_date = date.today()
    
    # Pass data from previous month to next 3 months
    months_to_graphs = []
    for rel in range(-1, 4):
        if rel == -1:
            months_to_graphs.append(current_date - relativedelta(months=1))
        else:
            months_to_graphs.append(current_date + relativedelta(months=rel))
    
    incomes = list(Income.objects.filter(user_id = request.user.id))
    fixed_incomes = FixedIncome.objects.filter(Q(end_month__isnull = True) | Q(end_month__lte = current_date), user_id = request.user.id)
    
    next_months_sum = {
        calendar.month_name[months_to_graphs[0].month]: 0,
        calendar.month_name[months_to_graphs[1].month]: 0,
        calendar.month_name[months_to_graphs[2].month]: 0,
        calendar.month_name[months_to_graphs[3].month]: 0,
        calendar.month_name[months_to_graphs[4].month]: 0,
    }

    
    for fincome in fixed_incomes:
        for i in range(-1, 4):
            fincome.created_at = current_date + relativedelta(months=i)
            next_months_sum[calendar.month_name[fincome.created_at.month]] += fincome.value
    
    for income in incomes:
        for month in months_to_graphs:
            if income.created_at.year == month.year and income.created_at.month == month.month:
                next_months_sum[calendar.month_name[income.created_at.month]] += income.value
    
    for key, value in next_months_sum.items():
        next_months_sum[key] = round(value, 2)
    
    return {
        "incomes_values_sum": next_months_sum.items(), 
        'incomes_values': list(next_months_sum.values()),
        }