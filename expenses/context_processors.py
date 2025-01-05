from datetime import date
from django.db.models import Sum
from .models import Expense, Income

def monthly_totals(request):
    if request.user.is_authenticated:
        today = date.today()
        first_day_of_month = today.replace(day=1)

        # Bu ayki gelir ve gider toplamları
        total_expenses = Expense.objects.filter(
            user=request.user,
            date__range=(first_day_of_month, today)
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_incomes = Income.objects.filter(
            user=request.user,
            date__range=(first_day_of_month, today)
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        return {
            'total_expenses': total_expenses,
            'total_incomes': total_incomes,
        }
    return {}
