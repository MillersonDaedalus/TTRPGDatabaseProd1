from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

def account_home(request):
    return render(request, 'account_home.html')

@login_not_required
def register(request):

    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages(request).success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'register.html', {'form': form})

@login_not_required
def about(request):
    return render(request, 'about.html')