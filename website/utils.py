from django.db.models import Q
from dateutil.relativedelta import relativedelta
import calendar

def get_expenses_summary(request, month_calendar, **models):
    current_date = month_calendar
    
    # Pass data from previous month to next 3 months
    months_to_graphs = []
    for rel in range(-1, 4):
        if rel == -1:
            months_to_graphs.append(current_date - relativedelta(months=1))
        else:
            months_to_graphs.append(current_date + relativedelta(months=rel))
    
    expenses = list(models['expenses'].objects.filter(user_id = request.user.id))
    fixed_expenses = models['fixed_expenses'].objects.filter(Q(end_month__isnull = True) | Q(end_month__lte = current_date), user_id = request.user.id)
    
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
    
def get_expense_category_data(request, month_calendar, **models):
    current_date = month_calendar
    
    expenses = list(models['expenses'].objects.filter(user_id = request.user.id))
    fixed_expenses = models['fixed_expenses'].objects.filter(Q(end_month__isnull = True) | Q(end_month__lte = current_date), user_id = request.user.id)

    category_sum = {}
    
    colors = ["#FF6384","#36A2EB","#FFCE56","#4BC0C0","#9966FF","#FF9F40","#FFCDCD","#C9CBCE","#FFE966","#66FFB2","#66B2FF", "#B266FF" ]
    
    
    for fexpense in fixed_expenses:
        try:
            category_sum[fexpense.category] += fexpense.value
        except KeyError:
            category_sum[fexpense.category] = fexpense.value
            
    for expense in expenses:
        try:
            category_sum[expense.category] += expense.value
        except KeyError:
            category_sum[expense.category] = expense.value
        
    return {
        'category_data_keys': list(category_sum.keys()),
        'category_data_values': list(category_sum.values()),
        'category_colors': colors[:len(category_sum)]
    }
    
def get_incomes_summary(request, month_calendar, **models):
    current_date = month_calendar
    
    # Pass data from previous month to next 3 months
    months_to_graphs = []
    for rel in range(-1, 4):
        if rel == -1:
            months_to_graphs.append(current_date - relativedelta(months=1))
        else:
            months_to_graphs.append(current_date + relativedelta(months=rel))
    
    incomes = list(models['incomes'].objects.filter(user_id = request.user.id))
    fixed_incomes = models['fixed_incomes'].objects.filter(Q(end_month__isnull = True) | Q(end_month__lte = current_date), user_id = request.user.id)
    
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