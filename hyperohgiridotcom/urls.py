from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hyperohgiridotcom.apps.public.urls')),
    path('accounts/', include('hyperohgiridotcom.apps.accounts.urls')),
]
