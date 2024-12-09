# processing/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Category, Expense
from django.contrib.auth import get_user_model
from .analysis import generate_savings_suggestion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Expense)
class ExpenseRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'category', 'date']
    list_filter = ['user', 'category', 'date']

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
            total_spending = qs.aggregate(total=Sum('amount'))['total'] or 0
            extra_context = extra_context or {}
            extra_context['total_spending'] = total_spending
            response.context_data.update(extra_context)
        except (AttributeError, KeyError):
            pass

        return response

    User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'predicted_future_spending', 'suggested_savings']

    def predicted_future_spending(self, obj):
        suggestion = generate_savings_suggestion(obj)
        return suggestion.get('predicted_future_spending', 'Bilgi yok')

    predicted_future_spending.short_description = "Tahmini Gelecek Harcaması"

    def suggested_savings(self, obj):
        suggestion = generate_savings_suggestion(obj)
        return suggestion.get('suggested_savings', 'Bilgi yok')

    suggested_savings.short_description = "Önerilen Tasarruf Miktarı"


admin.site.unregister(User)

admin.site.register(User, CustomUserAdmin)
