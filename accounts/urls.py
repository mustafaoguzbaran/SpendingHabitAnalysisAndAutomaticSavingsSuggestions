from django.urls import path
from .views import UserLoginView, UserLogoutView, register_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register_view, name='register'),
]
