from django.urls import path
from .views import expense_list_view, add_expense_view, savings_suggestion_view

urlpatterns = [
    path('', expense_list_view, name='expense_list'),
    path('add/', add_expense_view, name='add_expense'),
    path('suggestions/', savings_suggestion_view, name='savings_suggestion'),
]
