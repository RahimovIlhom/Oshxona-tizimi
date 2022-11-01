from django.urls import path
from .views import ChangeView

urlpatterns = [
    path('editing/', ChangeView.as_view(), name='editing'),
]