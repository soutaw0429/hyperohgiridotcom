from django.urls import path
from . import views

app_name="public"
urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('post', views.post, name="post"),
    path('over_comment/<int:comment_id>/', views.over_comment, name='over_comment'),
    path('over_like/<int:comment_id>/', views.over_like, name='over_like'),
    path('comment/<int:post_id>/', views.comment, name='comment'), 
    path('comment/<int:comment_id>/like_comment', views.like_comment, name='like_comment'),
    path('userInfo/<int:user_id>', views.user_info, name='user_info'),
    path('start', views.start_page, name='start_page')
]