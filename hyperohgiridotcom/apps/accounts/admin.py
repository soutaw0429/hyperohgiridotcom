from django.contrib import admin

from .models import UserProfile, UserPersona, UserInterest, Post, Comment

admin.site.register(UserProfile)
admin.site.register(UserPersona)
admin.site.register(UserInterest)
admin.site.register(Post)
admin.site.register(Comment)