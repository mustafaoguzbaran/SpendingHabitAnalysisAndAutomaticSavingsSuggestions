from django.shortcuts import render
from expenses.analysis import generate_savings_suggestion, get_monthly_spending_data, get_top_category

def index_view(request):
    if request.user.is_authenticated:
        suggestion_data = generate_savings_suggestion(request.user)
        predicted_future_spending = suggestion_data.get('predicted_future_spending', 0)
        suggested_savings = suggestion_data.get('suggested_savings', 0)

        labels, values = get_monthly_spending_data(request.user, months=6)
        last_month_spending = values[-1] if values else 0

        top_cat_name, top_cat_total = get_top_category(request.user)

        data = {
            'last_month_spending': last_month_spending,
            'predicted_future_spending': predicted_future_spending,
            'suggested_savings': suggested_savings,
            'top_category_name': top_cat_name,
            'top_category_total': top_cat_total,
            'username': request.user.username
        }
    else:
        data = {
            'last_month_spending': 0,
            'predicted_future_spending': 0,
            'suggested_savings': 0,
            'top_category_name': "Veri yok",
            'top_category_total': 0,
            'username': "Misafir"
        }

    return render(request, 'index.html', {'data': data})
