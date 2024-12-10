from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import UserSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
import string
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django import forms

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import RegisterForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tasks.models import Task

# users/views.py

from django.shortcuts import render, redirect

def home(request):
    print(f"User: {request.user}")  # Log the user object
    print(f"Is Authenticated: {request.user.is_authenticated}")  # Log the authentication status

    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to the dashboard if the user is authenticated
    return render(request, 'users/home.html')  # Render the home page if the user is not authenticated





class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

from django.shortcuts import render, redirect
from users.forms import RegisterForm
from users.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
             user = form.save(commit=False)
             user.set_password(form.cleaned_data['password'])  # Hash the password
             user.save()
             return redirect('login')
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{field}: {error.as_text()}")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
        
   
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f'Trying to authenticate user: {username} with password: {password}')  # Debug print
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f'User {username} authenticated successfully')  # Debug print
            login(request, user)
            return redirect('dashboard')
        else:
            print(f'Authentication failed for user: {username}')  # Debug print
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    return render(request, 'users/login.html')

 
from django.contrib.auth import authenticate, login, logout



@login_required
def dashboard(request):
    user_tasks = Task.objects.filter(user=request.user)
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='completed').count()
    pending_tasks = total_tasks - completed_tasks
    
    efficiency = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0


    return render(request, 'users/dashboard.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'efficiency': efficiency
    })


def custom_logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from datetime import timedelta
import random

User = get_user_model()

# Generate 6-digit OTP
def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

# Forget Password View
def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            user.reset_password_otp = otp
            user.reset_password_expiry = timezone.now() + timedelta(minutes=20)
            user.save()

            # Send OTP via email
            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP for password reset is {otp}. It is valid for 20 minutes.",
                from_email="noreply@yourproject.com",
                recipient_list=[email],
            )

            messages.success(request, "An OTP has been sent to your email.")
            return redirect(reverse("reset_password", kwargs={"user_id": user.id}))

        except User.DoesNotExist:
            messages.error(request, "No user is registered with this email.")
    return render(request, "users/forget_password.html")


import random
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PasswordReset, User

def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return redirect("request_password_reset")

        # Generate a 6-digit recovery code
        recovery_code = f"{random.randint(100000, 999999)}"
        valid_until = now() + timedelta(minutes=20)  # Code valid for 20 minutes

        # Save the recovery code in the database
        PasswordReset.objects.create(user=user, recovery_code=recovery_code, valid_until=valid_until)

        # Send the recovery code via email
        send_mail(
            subject="Password Reset Request",
            message=f"Your recovery code is: {recovery_code}. This code will expire in 20 minutes.",
            from_email="noreply@example.com",
            recipient_list=[user.email],
        )

        messages.success(request, "A recovery code has been sent to your email.")
        return redirect("confirm_password_reset")

    return render(request, "users/request_password_reset.html")


from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PasswordReset, User
from django.utils.timezone import now

def confirm_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        recovery_code = request.POST.get("recovery_code")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(email=email)
            password_reset = PasswordReset.objects.get(user=user, recovery_code=recovery_code)

            # Check if the recovery code is valid
            if password_reset.valid_until >= now():
                # Set the new password
                user.password = make_password(new_password)
                user.save()

                # Invalidate the recovery code
                password_reset.delete()

                messages.success(request, "Password has been reset successfully.")
                return redirect("login")
            else:
                messages.error(request, "Recovery code has expired. Request a new one.")
                return redirect("password_reset")

        except (User.DoesNotExist, PasswordReset.DoesNotExist):
            messages.error(request, "Invalid email or recovery code.")
            return redirect("confirm_password_reset")

    return render(request, "users/confirm_password_reset.html")
