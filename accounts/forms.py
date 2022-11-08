from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import EmployeeUser

class EmployeeUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = EmployeeUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'profession']

class EmployeeUserChangeForm(UserChangeForm):
    class Meta:
        model = EmployeeUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'profession']