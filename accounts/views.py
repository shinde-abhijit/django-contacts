from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserUpdateForm, LoginForm, ConfirmPasswordForm

title_tailwind_classes = " text-lg font-semibold uppercase text-center "




def homepage(request):
    user = request.user
    context = {
        'user': user,
        'title_tailwind_classes': title_tailwind_classes
    }
    return render(request, "accounts/homepage.html", context)




# Register
def register_view(request):
    user = request.user   
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    context = {
        'user': user,
        'form': form,
        'title_tailwind_classes': title_tailwind_classes
    }
    return render(request, 'accounts/register.html', context)


# Login
def login_view(request):    
    user = request.user
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    context = {
        'user': user,
        'form': form,
        'title_tailwind_classes': title_tailwind_classes
    }
    return render(request, 'accounts/login.html', context)


# Logout
@login_required
def logout_view(request):
    user = request.user
    if request.method == "POST":
        # User confirmed logout
        logout(request)
        messages.info(request, "Logged out successfully.")
        return redirect("login")
    
    context = {
        'user':user,
        'title_tailwind_classes': title_tailwind_classes
    }
    return render(request, "accounts/logout.html", context)


# Profile View
@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'title_tailwind_classes': title_tailwind_classes
    }
    return render(request, 'accounts/profile.html', context)


# Update Profile
@login_required
def update_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    context = {
        'user': user,
        'form': form,
        'title_tailwind_classes': title_tailwind_classes
    }
    return render(request, 'accounts/update_profile.html', context)


@login_required
def delete_profile_view(request):
    user = request.user

    if request.method == "POST":
        form = ConfirmPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user_check = authenticate(request, email=user.email, password=password)

            if user_check:
                logout(request)
                user.delete()
                messages.success(request, "Your account has been deleted.")
                return redirect('register')  # Or homepage
            else:
                messages.error(request, "Password is incorrect.")
    else:
        form = ConfirmPasswordForm()

    return render(request, "accounts/delete_profile.html", {
        "form": form,
        "user": user,
        "title_tailwind_classes": title_tailwind_classes
    })




