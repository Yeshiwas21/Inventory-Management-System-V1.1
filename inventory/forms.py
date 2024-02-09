# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import UserProfile, Storekeeper

class CustomUserCreationForm(UserCreationForm):
      class Meta:
        model = UserProfile
        fields = ['full_name', 'position', 'user_type', 'email', 'phone','username', 'password1', 'password2', 'image']

class CustomAuthenticationForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        choices=[
            ('normal', 'Normal User'),
            ('storekeeper', 'Store Keeper'),
            ('admin', 'Admin'),
        ],
        widget=forms.Select(attrs={'style': 'width: 200px;height: 30px; font-size: 20px;','class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'placeholder': 'Username', 'style': 'width: 300px; height: 40px;font-size: 20px;', 'class': 'form-control'})
        self.fields['password'].widget = PasswordInput(attrs={'placeholder' :'Password', 'style': 'width: 300px;height: 40px;font-size: 20px;', 'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user_type = cleaned_data.get('user_type')

        # Check if the provided username and user_type match an existing user
        try:
            user = UserProfile.objects.get(username=username, user_type=user_type)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError('Invalid username, password, or user type.')

        # Check if the provided password is correct
        if not user.check_password(password):
            raise forms.ValidationError('Invalid username, password, or user type.')

        return cleaned_data
    
    

class StorekeeperForm(forms.ModelForm):
    class Meta:
        model = Storekeeper
        fields = ['name']

