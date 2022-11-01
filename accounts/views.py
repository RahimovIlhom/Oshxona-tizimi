from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import EmployeeUserChangeForm


class ChangeView(CreateView):
    form_class = EmployeeUserChangeForm
    success_url = reverse_lazy('login')
    template_name = 'registration/editing.html'