from django.contrib import auth
from .models import MyUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
#from .models import UserProfile,ProfileSite


def login(request):
    return render(request, 'home/login.html')

def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return redirect('home:login')

    auth.login(request, user)
    return redirect('home:home')

def signup(request):
    return render(request, 'home/signup.html')

def signup_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    name = request.POST.get('name')
    gender = request.POST.get('gender')
    try:

        user = MyUser.objects.create_user(username=username, password=password, email=email, gender=gender, name=name)

        user = auth.authenticate(request, username=username, password=password)
        auth.login(request, user)
        return redirect('home:home')

    except:
        return redirect('home:signup')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home:login')