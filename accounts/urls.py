from django.urls import path
from .views import ChangeUserView, CreateUserView, AdminUserChangeView, all_users_view, delete_user_view

urlpatterns = [
    path('editing/<int:pk>/', ChangeUserView.as_view(), name='editing'),
    path('admin/adduser/', CreateUserView.as_view(), name='adduser'),
    path('admin/users/', all_users_view, name='users'),
    path('admin/user/edit/<int:pk>', AdminUserChangeView.as_view(), name='admin_edit'),
    path('admin/user/delete/<username>', delete_user_view, name='delete_user'),
]