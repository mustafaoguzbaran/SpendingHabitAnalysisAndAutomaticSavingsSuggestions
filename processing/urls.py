from django.urls import path
from .views import user_spending_stats_view

urlpatterns = [
    path('user-spending-stats/', user_spending_stats_view, name='user_spending_stats'),
]

