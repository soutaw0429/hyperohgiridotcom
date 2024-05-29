from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name="accounts"
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name="profile"),

    #add profile
    path('add_profile/', views.add_profile, name='add_profile'),

    #Django auth
    path('login', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    #register
    path('register', views.register_user, name='register_user'),
    path('register_email/', views.register_email, name='register_email'),
    path('verify_email/', views.verify_email, name='verify_email'),

    #password reset
    path('forget_password/', views.forget_password, name='forget_password'),
    path('reset_password/<uidb64>/<token>/', views.CustomPasswordResetView.as_view(), name='password_reset_confirm'),
    path('reset_password/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #other
    path('ask_add_profile/', views.ask_add_profile, name='ask_add_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
