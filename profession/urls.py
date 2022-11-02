from django.urls import path
from .views import professions_page

urlpatterns = [
    path('', professions_page, name='profession'),
]