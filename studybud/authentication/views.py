from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import User
from .forms import MyUserCreationForm


# dont call it login, becuase we have a function called login
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist...')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # create session in the database, and save session key in browser cooki for that user
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or passwrod dose not exists...')

    context = {'page': page}
    return render(request, 'auth/login_register.html', context)


@login_required(login_url='/auth')
def logoutUser(request):
    logout(request)

    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            # if user added like upper case in their or capitalize thier name or maybe their email, we want to make sure that lowercase automatically or clean this data
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error occured during registration...')

    context = {'form': form}
    return render(request, 'auth/login_register.html', context)
