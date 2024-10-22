from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Expense, FixedExpense, Income, FixedIncome

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''
    
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = None
    
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].label = ''
    
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].label = ''
    
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['arial-describedby'] = 'passwordHelpInline'
        self.fields['password1'].help_text = '''
            <small id="passwordHelpInline" class="text-muted">
                <span>Your password can’t be too similar to your other personal information.</span><br>
                <span>Your password must contain at least 8 characters.</span><br>
                <span>Your password can’t be a commonly used password.</span><br>
                <span>Your password can’t be entirely numeric.</span><br>
            </small>
        '''
    
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = None
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        
class AddExpenseForm(forms.ModelForm):
    created_at = forms.DateField(required=True,widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }))
    created_at.label = 'Date'
    
    category = forms.ChoiceField(choices={
        'food': 'Food',
        'home': 'Home',
        'transport': 'Transport',
        'taxes': 'Taxes',
        'bills': 'Fixed bills(Energy, Water, Gas, etc...)',
        'entertainment': 'Entertainment',
        'study': 'Study',
        'eletronics': 'Eletronics',
        'clothes': 'Clothes',
        'health': 'Health',
        'investments': 'Investments',
        'others': 'Others'
    })
    category.widget.attrs['class'] = 'form-control'
    
    name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    
    description = forms.CharField(required=True, max_length=250, widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    
    value = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }))
    
    type = forms.ChoiceField(choices={
        'in_cash': 'In cash',
        'installments': 'Installments',
        'fixed': 'Fixed'
    })
    type.widget.attrs['class'] = 'form-control'
    
    installments = forms.IntegerField(required=True,initial=1, min_value=1, widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }))
    
    class Meta:
        model = Expense
        exclude = ['user']
        fields = ['created_at', 'category', 'name', 'description', 'value', 'type', 'installments']
        
class AddFixedExpenseForm(forms.ModelForm):
    created_at = forms.DateField()
    category = forms.CharField()
    name = forms.CharField()
    description = forms.CharField()
    value = forms.DecimalField()
    end_month = forms.DateField(required=False)
    
    class Meta:
        model = FixedExpense
        exclude = ['user', 'end_month']
        
class AddIncomeForm(forms.ModelForm):
    created_at = forms.DateField(required=True,widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }))
    created_at.label = 'Date'
    
    category = forms.ChoiceField(choices={
        'salary': 'Salary',
        'investments': 'Investments',
        'rentals': 'Rentals',
        'bonus': 'Bonus',
        'extra-income': 'Extra Income',
        'others': 'Others',
    })
    category.widget.attrs['class'] = 'form-control'
    
    name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    
    description = forms.CharField(required=True, max_length=250, widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    
    value = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }))
    
    class Meta:
        model = Income
        exclude = ['user']
        fields = ['created_at', 'category', 'name', 'description', 'value']
    
class AddFixedIncomeForm(forms.ModelForm):
    created_at = forms.DateField()
    category = forms.CharField()
    name = forms.CharField()
    description = forms.CharField()
    value = forms.DecimalField()
    end_month = forms.DateField(required=False)
    
    class Meta:
        model = FixedIncome
        exclude = ['user', 'end_month']