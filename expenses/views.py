# expenses/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .analysis import generate_savings_suggestion, get_monthly_spending_data
from .models import Expense, Income
from .forms import ExpenseForm, IncomeForm
from django.db.models import Sum
from datetime import date, timedelta


@login_required
def expense_list_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def add_expense_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})


@login_required
def savings_suggestion_view(request):
    suggestion = generate_savings_suggestion(request.user)
    return JsonResponse(suggestion)

@login_required
def monthly_spending_chart(request):
    user = request.user
    today = date.today()
    one_month_ago = today - timedelta(days=30)
    three_months_ago = today - timedelta(days=90)
    one_year_ago = today - timedelta(days=365)

    def get_data(start_date, end_date=today):
        expenses = (
            Expense.objects.filter(user=user, date__range=(start_date, end_date))
            .values('date__year', 'date__month')
            .annotate(total=Sum('amount'))
            .order_by('date__year', 'date__month')
        )
        incomes = (
            Income.objects.filter(user=user, date__range=(start_date, end_date))
            .values('date__year', 'date__month')
            .annotate(total=Sum('amount'))
            .order_by('date__year', 'date__month')
        )

        expense_data = {f"{e['date__year']}-{e['date__month']:02d}": float(e['total']) for e in expenses}
        income_data = {f"{i['date__year']}-{i['date__month']:02d}": float(i['total']) for i in incomes}
        all_dates = sorted(set(expense_data.keys()) | set(income_data.keys()))

        expense_values = [expense_data.get(d, 0) for d in all_dates]
        income_values = [income_data.get(d, 0) for d in all_dates]

        return all_dates, expense_values, income_values

    # 1 Aylık, 3 Aylık, ve 1 Yıllık Verileri Al
    one_month_labels, one_month_expenses, one_month_incomes = get_data(one_month_ago)
    three_months_labels, three_months_expenses, three_months_incomes = get_data(three_months_ago)
    one_year_labels, one_year_expenses, one_year_incomes = get_data(one_year_ago)

    return render(request, 'expenses/monthly_spending_chart.html', {
        'one_month_labels': one_month_labels,
        'one_month_expenses': one_month_expenses,
        'one_month_incomes': one_month_incomes,
        'three_months_labels': three_months_labels,
        'three_months_expenses': three_months_expenses,
        'three_months_incomes': three_months_incomes,
        'one_year_labels': one_year_labels,
        'one_year_expenses': one_year_expenses,
        'one_year_incomes': one_year_incomes,
    })



@login_required
def add_income_view(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Giriş yapan kullanıcıya bağla
            income.save()
            return redirect('income_list')  # Gelir listesine yönlendirme
    else:
        form = IncomeForm()
    return render(request, 'expenses/add_income.html', {'form': form})

@login_required
def income_list_view(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')  # Kullanıcıya özel gelirler
    return render(request, 'expenses/income_list.html', {'incomes': incomes})
