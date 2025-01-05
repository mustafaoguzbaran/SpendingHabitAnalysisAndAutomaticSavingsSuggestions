from django.urls import path
from .views import expense_list_view, add_expense_view, savings_suggestion_view, monthly_spending_chart, \
    add_income_view, income_list_view

urlpatterns = [
    path('', expense_list_view, name='expense_list'),
    path('add/', add_expense_view, name='add_expense'),
    path('suggestions/', savings_suggestion_view, name='savings_suggestion'),
    path('monthly-chart/', monthly_spending_chart, name='monthly_spending_chart'),
    path('add-income/', add_income_view, name='add_income'),
    path('income-list/', income_list_view, name='income_list'),
]
