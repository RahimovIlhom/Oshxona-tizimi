from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import EmployeeUserChangeForm, EmployeeUserCreateForm
from .models import EmployeeUser

# Register your models here.

class EmployeeUserAdmin(UserAdmin):
    add_form = EmployeeUserCreateForm
    form = EmployeeUserChangeForm
    model = EmployeeUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age',)}),
    )

admin.site.register(EmployeeUser, EmployeeUserAdmin)