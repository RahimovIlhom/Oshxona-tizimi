from django.urls import path
from .views import ChangeUserView, CreateUserView

urlpatterns = [
    path('editing/<int:pk>/', ChangeUserView.as_view(), name='editing'),
    path('adduser/', CreateUserView.as_view(), name='adduser'),
]