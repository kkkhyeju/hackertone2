from django.db import models
from django.contrib.auth.models import User  
from django.db.models.signals import post_save  
from django.dispatch import receiver

class Answer(models.Model):
    userName = models.CharField(max_length = 20)
    question = models.TextField()
    answerlist = models.TextField()
    
class Team(models.Model):
    teamname = models.CharField(max_length = 20)
    howlong = models.IntegerField()
    questionlist = models.TextField()
    userlist = models.TextField()
    teamcode = models.CharField(max_length = 10)

class Profile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.CharField(max_length = 20)
    teamcheck = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

class Question(models.Model):  
    title = models.TextField()
    body = models.TextField()
    
    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()
