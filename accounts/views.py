from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import EmployeeUser
from .forms import EmployeeUserChangeForm, EmployeeUserCreateForm


class ChangeUserView(UpdateView, LoginRequiredMixin):
    model = EmployeeUser
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'registration/editing.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

class CreateUserView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    form_class = EmployeeUserCreateForm
    template_name = 'registration/adduser.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def test_func(self):
        return self.request.user.is_superuser