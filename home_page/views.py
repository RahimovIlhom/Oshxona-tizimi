from django.shortcuts import render, redirect

# Create your views here.

def redirect_login(request):
    response = redirect('accounts/login/')
    return response