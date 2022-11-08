from django.shortcuts import render, redirect
from django.contrib import messages

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
