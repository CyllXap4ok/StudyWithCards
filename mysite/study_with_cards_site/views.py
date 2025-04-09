from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserSignInForm, UserSignUpForm

@login_required(login_url='sign_in')
def home_view(request):
    return render(request, 'home.html')

def signin_view(request):
    if request.method == 'POST':
        form = UserSignInForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Form validation error")
    else:
        form = UserSignInForm()

    return render(request, 'sign_in.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
    else:
        form = UserSignUpForm()

    return render(request, 'sign_up.html', {'form': form})

def cards_creation_view(request):
    return render(request, 'cards_creation.html')

def cards_study_view(request):
    return render(request, 'cards_study.html')

def stats_view(request):
    return render(request, 'stats.html')
