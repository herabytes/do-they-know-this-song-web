from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    score = models.IntegerField()
    
    def __str__(self):
        return self.username +' (' + self.score + ")"

class Game(models.Model): 
    track = models.CharField(max_length=20) #mbid as string
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player")
    correct = models.BooleanField()
    