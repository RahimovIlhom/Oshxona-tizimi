from django.shortcuts import render, redirect

# Create your views here.

def redirect_login(request):
    if request.user.is_authenticated:
        response = redirect('profession')
    else:
        response = redirect('accounts/login/')
    return response

def redirect_404_found(request):
    return render(request, 'found_404.html',{

    })