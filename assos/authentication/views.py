from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from authentication.forms import ProfilePhotoForm
from django.contrib.auth.decorators import login_required

from . import forms

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'login.html', context={'form': form, 'message': message})

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('index')
    return render(request, 'signup.html', context={'form': form})

@login_required
def photoprofil_upload(request):
    form = ProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'photoprofil_upload.html', context={'form': form})


