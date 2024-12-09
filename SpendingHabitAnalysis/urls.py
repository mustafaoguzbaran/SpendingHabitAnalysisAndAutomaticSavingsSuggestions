from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.http import HttpResponse

from SpendingHabitAnalysis.views import index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('expenses/', include('expenses.urls')),
]
