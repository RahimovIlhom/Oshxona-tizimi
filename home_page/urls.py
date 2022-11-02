from .views import redirect_login
from django.urls import path

urlpatterns = [
    path('', redirect_login, name='login'),
]
