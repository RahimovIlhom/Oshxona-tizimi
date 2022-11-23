from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import EmployeeUser
from .forms import EmployeeUserChangeForm, EmployeeUserCreateForm
# from django.contrib.auth import logout
# import datetime

# from core.settings import SESSION_IDLE_TIMEOUT
# from django.conf import settings
# import codesettings


class ChangeUserView(LoginRequiredMixin, UpdateView):
    model = EmployeeUser
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'registration/editing.html'
    success_url = reverse_lazy('profession')


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = EmployeeUserCreateForm
    template_name = 'admin_page/adduser.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser



# class SessionIdleTimeout(object):
#     """Middle ware to ensure user gets logged out after defined period if inactvity."""
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#
#         if request.user.is_authenticated:
#             current_datetime = datetime.datetime.now()
#
#             if 'last_active_time' in request.session:
#                 idle_period = (current_datetime -
#                                request.session['last_active_time']).seconds
#                 if idle_period > settings.SESSION_IDLE_TIMEOUT:
#                     logout(request)
#                     response = redirect('/accounts/login/')
#                     response.delete_cookie('username')
#                     return response
#             request.session['last_active_time'] = current_datetime
#
#         response = self.get_response(request)
#         return response


class AdminUserChangeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmployeeUser
    fields = ['username', 'first_name', 'last_name', 'email', 'profession', 'phone']
    template_name = 'admin_page/edit_user.html'
    success_url = reverse_lazy('users')

    def test_func(self):
        return self.request.user.is_superuser

@login_required
def all_users_view(request):
    if request.user.is_superuser or request.user.profession == 'accountant':
        all_users = EmployeeUser.objects.all()
        return render(request, 'admin_page/users.html', {
            'users': all_users,
        })
    else:
        return redirect('/page/not_found/')


# class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = EmployeeUser
#     template_name = 'admin_page/deleteuser.html'
#     success_url = reverse_lazy('users')
#
#     def test_func(self):
#         return self.request.user.is_superuser