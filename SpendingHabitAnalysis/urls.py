from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Anasayfaya Hoş Geldiniz!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('expenses/', include('expenses.urls')),
    path('data/', include('processing.urls')),
]
