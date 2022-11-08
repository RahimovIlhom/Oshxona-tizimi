from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import EmployeeUser
from .forms import EmployeeUserChangeForm, EmployeeUserCreateForm


class ChangeUserView(UpdateView, LoginRequiredMixin):
    model = EmployeeUser
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'registration/editing.html'
    success_url = reverse_lazy('profession')


class CreateUserView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    form_class = EmployeeUserCreateForm
    template_name = 'admin_page/adduser.html'
    success_url = reverse_lazy('users')

    def test_func(self):
        return self.request.user.is_superuser


class AdminUserChangeView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = EmployeeUser
    fields = ['username', 'first_name', 'last_name', 'email', 'profession', 'phone']
    template_name = 'admin_page/edit_user.html'
    success_url = reverse_lazy('users')

    def test_func(self):
        return self.request.user.is_superuser


def all_users_view(request):
    if request.user.is_superuser:
        all_users = EmployeeUser.objects.all()
        return render(request, 'admin_page/users.html', {
            'users': all_users,
        })
    else:
        return redirect('/page/not_found/')


class DeleteUserView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = EmployeeUser
    template_name = 'admin_page/deleteuser.html'
    success_url = reverse_lazy('users')

    def test_func(self):
        return self.request.user.is_superuser