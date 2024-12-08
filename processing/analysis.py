from .models import ExpenseRecord
from django.db.models import Avg, Sum


def get_user_spending_stats(user):
    data = ExpenseRecord.objects.filter(user=user)
    total_spending = data.aggregate(total=Sum('amount'))['total'] or 0
    avg_spending = data.aggregate(avg=Avg('amount'))['avg'] or 0

    spending_by_category = data.values('category').annotate(
        total=Sum('amount'),
        avg=Avg('amount')
    )

    return {
        'total_spending': total_spending,
        'avg_spending': avg_spending,
        'spending_by_category': list(spending_by_category)
    }
