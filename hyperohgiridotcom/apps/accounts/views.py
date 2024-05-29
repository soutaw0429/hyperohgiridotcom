import random
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile, User, UserPersona, UserInterest
from .forms import UserRegistrationForm, UserProfileForm, UserForm, EmailForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
import logging
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)

       

def register_user(request):
        if request.method == 'POST':
                form = UserRegistrationForm(request.POST)
                if form.is_valid():
                        user = form.save()
                        profile = UserProfile(user=user)
                        profile.save()

                        login(request, user)
                        return redirect('accounts:register_email')
                else:
                        messages.error(request,"ユーザーの作成に失敗しました。")

        else:
                form = UserRegistrationForm()

        return render(request, 'accounts/register.html', {'form': form})

@login_required
def register_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']

            verification_code = ''.join(random.choices('0123456789', k=4))

            request.session['email_verification_code'] = verification_code
            request.session['email_to_verify'] = email
            send_verification_email(email, verification_code)
            messages.success(request, "入力いただいたメールアドレスに認証コードを送信しました。")
            return redirect('accounts:verify_email')
        else:
            messages.error(request, "メールアドレスのフォーマットが正しくありません。もう一度入力を行なってください。")
    else:
        email_form = EmailForm()
    
    return render(request, 'accounts/register_email.html', {'form': email_form})

def send_verification_email(email, verification_code):
       subject ='[ハイパーオーギリドットコム] メールアドレス2段階認証のお願い'
       message = f'こちらが4桁の認証コードになります。: {verification_code}' 
       from_email = 'pinestudio0224@gmail.com'
       send_mail(subject, message, from_email, [email])

def verify_email(request):
       if request.method == 'POST':
              entered_code = request.POST.get('verification_code', '')
              session_code = request.session.get('email_verification_code', '')
              email_to_verify =request.session.get('email_to_verify', '')
              if entered_code == session_code:
                     user = request.user
                     user_profile, created = UserProfile.objects.get_or_create(user=user)
                     user_profile.email = email_to_verify
                     user_profile.save()
                     del request.session['email_verification_code']
                     del request.session['email_to_verify']
                     messages.success(request, "2段階認証が完了しました。")
                     return redirect('accounts:ask_add_profile')
              else:
                     messages.error(request, "認証コードが正しくありません。")
                     return redirect('accounts:verify_email')
       else:
              return render(request, 'accounts/verify_email.html')
                     
                     
        


                     

def ask_add_profile(request):
       return render(request, 'accounts/ask_add_profile.html')

                        

@login_required
def add_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_instance = request.user

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        user_form = UserForm(request.POST, instance=user_instance)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()

            interests_names = request.POST.getlist('interests')

            persona_id = request.POST.get('persona')
            if persona_id:
                user_profile.persona = UserPersona.objects.get(id=persona_id)

            if interests_names:
                user_profile.interests.set(interests_names)

            user_profile.save()

            return redirect('accounts:profile')  # Redirect to the profile page after saving

    else:
        profile_form = UserProfileForm(instance=user_profile)
        user_form = UserForm(instance=user_instance)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
        'user_instance':user_instance
    }
    return render(request, 'accounts/add_profile.html', context)

def profile_view(request):
        return render(request, 'profile.html') 

def forget_password(request):
        if request.method == 'POST':
                email = request.POST.get('email')
                if send_password_reset_email(request, email):
                        messages.success(request, "パスワード変更用のメールが送信されました。")
                else:
                        messages.success(request, "入力いただいたメールアドレスを登録しているユーザーが見つかりませんでした。")
                return redirect('accounts:forget_password')
        return render(request, 'accounts/forget_password.html')

def send_password_reset_email(request, email):
        try:
                user_profile_instance = UserProfile.objects.get(email=email)
                user = user_profile_instance.user
                current_site = get_current_site(request)
                email_subject = '[ハイパーオーギリドットコム] パスワード更新のお願い。'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                reset_link = f'http://{current_site.domain}{reset_url}'

                context = {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': uid,
                        'token': token,
                        'reset_link': reset_link,
                }
                logger.info(f'Email context: {context}')
                message = render_to_string('accounts/password_reset_email.html', context)

                send_mail(
                        email_subject,
                        message,
                        'pinestudio0224@gmail.com',
                        [email],
                        fail_silently=False,
                )

                return True
        except UserProfile.DoesNotExist:
                return False



class CustomPasswordResetView(PasswordResetConfirmView):
        template_name = 'accounts/password_reset.html'

        def form_valid(self, form):
                new_password1 = form.cleaned_data['new_password1']
                new_password2 = form.cleaned_data['new_password2']
                if new_password1 != new_password2:
                        messages.error(self.request, "Passwords do not match.")
                        return self.form_invalid(form)
                
                return super().form_valid(form)             
        success_url = reverse_lazy('accounts:login')
        success_message = "新規パスワードの設定が完了しました。"
        

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
        template_name = 'accounts/password_reset_complete.html'
                

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
        



