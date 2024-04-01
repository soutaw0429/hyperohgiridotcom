from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile, User
from .forms import UserRegistrationForm, UserProfileForm, UserForm
#from . import views
       

def register_user(request):
        if request.method == 'POST':
                form = UserRegistrationForm(request.POST)
                if form.is_valid():
                        user = form.save()
                        profile = UserProfile(user=user)
                        profile.save()

                        login(request, user)
                        return redirect('public:index')
        else:
                form = UserRegistrationForm()

        return render(request, 'accounts/register.html', {'form': form})

def add_profile(request):
        user_profile = UserProfile.objects.get(user=request.user)
        user_instance = User.objects.get(username=request.user.username)
        if request.method == 'POST':
                user_form = UserForm(request.POST, instance=user_instance)
                profile_form = UserProfileForm(request.POST, instance=user_profile)
                if user_form.is_valid() and profile_form.is_valid():
                        user_form.save()
                        profile_form.save()
                        return redirect('accounts:profile')
        else:
                user_form = UserForm(instance=user_instance)
                profile_form = UserProfileForm(instance=user_profile)
        return render(request, 'accounts/add_profile.html', {'user_form':user_form, 'profile_form':profile_form})

def profile_view(request):
        return render(request, 'profile.html')                

                

class ProfileView(LoginRequiredMixin, TemplateView):
        template_name = 'accounts/profile.html'

        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                user = self.request.user

                try:
                        profile = UserProfile.objects.get(user=user)
                except UserProfile.DoesNotExist:
                        profile = None

                context['profile'] = profile

                return context
        



