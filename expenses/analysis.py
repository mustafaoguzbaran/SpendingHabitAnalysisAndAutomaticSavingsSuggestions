import datetime
from django.db.models import Sum
from datetime import date, timedelta

from .models import Expense
from sklearn.linear_model import LinearRegression
import numpy as np


def generate_savings_suggestion(user):

    year_month_expenses = (
        Expense.objects
        .filter(user=user)
        .values('date__year', 'date__month')
        .annotate(monthly_total=Sum('amount'))
        .order_by('date__year', 'date__month')
    )

    if not year_month_expenses:
        return {"suggestion": "Veri bulunamadı. Tasarruf önerisi yapılamıyor."}

    X = []
    y = []
    month_count = 1
    for record in year_month_expenses:
        X.append([month_count])
        y.append(record['monthly_total'])
        month_count += 1

    X = np.array(X)
    y = np.array(y)

    model = LinearRegression()
    model.fit(X, y)

    next_month_index = month_count

    future_spending_pred = model.predict([[next_month_index]])[0]

    saving_suggestion = future_spending_pred * 0.1

    return {
        "predicted_future_spending": round(float(future_spending_pred), 2),
        "suggested_savings": round(float(saving_suggestion), 2),
        "suggestion": f"Gelecek ay tahmini harcamanız {future_spending_pred:.2f} TL. " \
                      f"Bu tutardan yaklaşık {saving_suggestion:.2f} TL tasarruf edebilirsiniz."
    }


def get_monthly_spending_data(user, months=6):
    today = date.today()
    start_date = today - datetime.timedelta(days=months * 30)

    data = (
        Expense.objects
        .filter(user=user, date__gte=start_date, date__lte=today)
        .values('date__year', 'date__month')
        .annotate(total=Sum('amount'))
        .order_by('date__year', 'date__month')
    )

    labels = []
    values = []
    for record in data:
        year = record['date__year']
        month = record['date__month']
        total = record['total']
        labels.append(f"{year}-{month:02d}")
        values.append(float(total))

    return labels, values
