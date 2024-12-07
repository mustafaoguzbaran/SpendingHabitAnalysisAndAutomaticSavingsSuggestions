from django.urls import path
from .views import UserLoginView, UserLogoutView, register_view

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
]
