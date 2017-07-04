from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile,ProfileSite


def login(request):
    return render(request, 'home/login.html')

def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return redirect('home:login')

    auth.login(request, user)

    '''
    uu = request.user
    uu.userprofile.name = "changed"
    uu.userprofile.save()
    '''
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
        user = User.objects.create_user(username=username, password=password, email=email)
        profile = UserProfile()
        profile.user = user
        profile.name = name
        profile.gender = gender
        profile.save()

        profile_site = ProfileSite()
        profile_site.user = user
        profile_site.user_id = user.id
        profile_site.username = username
        profile_site.name = name
        profile_site.email = email
        profile_site.gender = gender
        profile_site.save()
        return redirect('home:login')

    except:
        return redirect('home:signup')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home:login')