from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from products.models import Category, Product
from accounts.models import EmployeeUser


def professions_page(request):
    if request.user.is_authenticated:
        return render(request, 'profession.html', {
        })
    else:
        response = redirect('/accounts/login/')
        return response

def cashier_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.profession == 'cashier':
            all_category = Category.objects.all()
            products = []
            for category in all_category:
                products.append(Product.objects.filter(category=category))
            return render(request, 'profession-cashier.html', {
                'categories': all_category,
                'c_products': products,
            })
        else:
            return redirect('/page/not_found/')
    else:
        response = redirect('/accounts/login/')
        return response


def accountant_view(request):
    if request.user.is_superuser or request.user.profession == 'accountant':

        return render(request, 'admin_page/home.html', {

        })
    else:
        return redirect('/page/not_found/')


def categories_view(request):
    if request.user.is_superuser:
        all_categoies = Category.objects.all()

        return render(request, 'admin_page/categories.html', {
            'categories': all_categoies,
        })
    else:
        return redirect('/page/not_found/')

class CategoryCreateView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Category
    template_name = 'admin_page/create_category.html'
    fields = ['name', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

class CategoryUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Category
    template_name = 'admin_page/update_category.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser


class CategoryDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Category
    template_name = 'admin_page/delete_category.html'
    success_url = reverse_lazy('categories')

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser


def products_view(request):
    if request.user.is_superuser:
        products = Product.objects.all()

        return render(request, 'admin_page/products.html', {
            'categories': products,
        })
    else:
        return redirect('/page/not_found/')

class ProductCreateView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Product
    template_name = 'admin_page/create_product.html'
    fields = ['name', 'price', 'discount_price', 'category',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

class ProductUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Product
    template_name = 'admin_page/update_product.html'
    fields = ['name', 'price', 'discount_price', 'category',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser