from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/dashboard/')  # or use: return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # This should match the name in your urls.py

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

      

        # You'll need a custom user model or profile model for phone_number
        # Otherwise, skip this check or manage it separately

        # Create user (store full_name as first_name for now)
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=full_name,



            
        )
        user.save()

        messages.success(request, 'User created successfully! Please log in.')
        return redirect('login')

    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')



def home(request):
    return render(request, 'home.html')

