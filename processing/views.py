from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .analysis import get_user_spending_stats

@login_required
def user_spending_stats_view(request):
    user = request.user
    stats = get_user_spending_stats(user)
    return JsonResponse(stats)
