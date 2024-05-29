from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_image', 'is_full_name_displayed', 'bio', 'website', 'persona', 'interests']
        required = {'website': False}

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class EmailForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', max_length=254, required=True)
