# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserProfile
from django.db import transaction
from django.views.generic import View
import pdb



def index(request):
    return render(request, 'index.html')

def register_user(request):
    if request.method == 'POST':
        user_register_form = CustomUserCreationForm(request.POST, request.FILES)
        if user_register_form.is_valid():
            user_register_form.save()
            messages.success(request, 'User Profile created successfully!')
            return redirect('user_list')
    else:
        user_register_form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'user_register_form': user_register_form})


def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        edit_user_form = CustomUserCreationForm(request.POST, instance=user)

        if edit_user_form.is_valid():
            user = edit_user_form.save(commit=False)
            # Additional logic if needed
            user.save()
            messages.success(request, f'{user.full_name} updated successfully.')
            return redirect('product_list')
    else:
        edit_user_form = CustomUserCreationForm(instance=user)

    return render(request, 'users/edit_user.html', {'edit_user_form': edit_user_form, 'user': user})

class DeleteUserView(View):
    def post(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(UserProfile, id=user_id)
        user.delete()
        messages.success(request, f'{user.full_name} has been deleted successfully.')
        return redirect('user_list')

    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(UserProfile, id=user_id)
        return render(request, 'users/delete_user.html', {'user': user})


@login_required
def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def custom_login(request):
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username'] 
            password = login_form.cleaned_data['password']
            user_type = login_form.cleaned_data['user_type']

            user = authenticate(
                request, 
                username=username, 
                password=password,
                user_type=user_type
            )
            if user is not None:
                login(request, user)
                if user_type == 'normal':
                    messages.success(request, 'Logged in successfully.')
                    return redirect('index')
                elif user_type == 'storekeeper':
                    messages.success(request, 'Logged in successfully.')
                    return redirect('store_keeper')
                elif user_type == 'admin':
                    messages.success(request, 'Logged in successfully.')
                    return redirect('admin_view')
            else:
                messages.error(request, 'Invalid username, password, or user type.')
    else:
        login_form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'login_form': login_form})


@transaction.atomic
def custom_logout(request):
    # Add any custom actions you want before logging out

    # Log out the user
    logout(request)

    # Redirect to a specific page after logout
    return render(request, 'products/logout.html')
