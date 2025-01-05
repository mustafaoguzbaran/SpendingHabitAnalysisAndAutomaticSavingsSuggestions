import datetime
from django.db.models import Sum
from datetime import date, timedelta
from .models import Expense, Category
from sklearn.linear_model import LinearRegression
import numpy as np

def generate_savings_suggestion(user):
    categories = Category.objects.all()
    category_weights = {cat.id: cat.weight for cat in categories}

    monthly_category_expenses = (
        Expense.objects
        .filter(user=user)
        .values('date__year', 'date__month', 'category')
        .annotate(monthly_total=Sum('amount'))
        .order_by('date__year', 'date__month')
    )

    if not monthly_category_expenses:
        return {"suggestion": "Veri bulunamadı. Tasarruf önerisi yapılamıyor."}

    monthly_data = {}

    for record in monthly_category_expenses:
        year = record['date__year']
        month = record['date__month']
        cat_id = record['category']
        total = record['monthly_total']

        weight = category_weights.get(cat_id, 1.0)
        weighted_value = float(total) * float(weight)

        monthly_data.setdefault((year, month), 0)
        monthly_data[(year, month)] += weighted_value

    X = []
    y = []
    month_count = 1

    for (year, month) in sorted(monthly_data.keys()):
        X.append([month_count])
        y.append(monthly_data[(year, month)])
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
        "suggestion": f"Gelecek ay tahmini harcamanız {future_spending_pred:.2f} TL (kategori ağırlıklı). " \
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

def get_top_category(user):
    top_cat = (
        Expense.objects
        .filter(user=user)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )
    if top_cat:
        return top_cat['category__name'], float(top_cat['total'])
    return None, 0.0
