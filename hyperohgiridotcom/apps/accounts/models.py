from django.db import models
from django.contrib.auth.models import User

class UserInterest(models.Model):
    name = models.CharField(max_length=64, unique=True)
    normalized_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name



class UserPersona(models.Model):
    name = models.CharField(max_length=64, unique=True)
    normalized_name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length = 200)

    def __str__(self):
        return self.name



# Create your models here.
class UserProfile(models.Model):

    #owner
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    #settings
    is_full_name_displayed = models.BooleanField(default=True)

    #details
    bio = models.CharField(max_length=500, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    persona = models.ForeignKey(UserPersona, on_delete=models.SET_NULL, blank=True, null=True)
    interests = models.ManyToManyField(UserInterest, blank=True)

    
    # Zabutons received by the user(Zabuton = Like)
    total_zabutons_received = models.PositiveIntegerField(default=0)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_comments = models.IntegerField(default=0)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    num_zabutons = models.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ['user', 'post']  # Ensures a user can only comment once on a post

class Zabuton(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'comment']  # Ensures a user can only like one comment per post




