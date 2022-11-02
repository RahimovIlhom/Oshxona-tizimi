from django.urls import path
from .views import professions_page, cashier_view

urlpatterns = [
    path('', professions_page, name='profession'),
    path('cashier/', cashier_view, name='cashier'),
]