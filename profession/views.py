from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Profession
from products.models import Category, Product


def professions_page(request):
    all_profession = Profession.objects.all()
    return render(request, 'profession.html', {
        'professions': all_profession,
    })

def first_pro_page(request):
    first_profession = Profession.objects.all()[0]
