# expenses/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .analysis import generate_savings_suggestion, get_monthly_spending_data
from .models import Expense
from .forms import ExpenseForm

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
    labels, values = get_monthly_spending_data(request.user, months=6)
    return render(request, 'expenses/monthly_spending_chart.html', {
        'labels': labels,
        'values': values
    })