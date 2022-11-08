from .views import redirect_login, redirect_404_found
from django.urls import path

urlpatterns = [
    path('', redirect_login, name='login'),
    path('page/not_found/', redirect_404_found, name='not_found')
]
