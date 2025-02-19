from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    likes = models.ManyToManyField(User,symmetrical=False, blank=True, related_name='like')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Post by {self.user} on {self.timestamp.strftime("%d %b %Y %H:%M:%S")}'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    user_to_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    
    
    def __str__(self) -> str:
        return f'{self.user} follows {self.user_to_follow}'