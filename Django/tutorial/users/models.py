from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid

# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver # imported it to use decorator


 

# profile model -- here we will create our profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True,)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default= "profiles/user-default.png")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)
    

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return str(self.name) 
    

class Message(models.Model):
#BLANK=TRUE---->MEANS NOT REGISTERED USER CAN ALSO SEND THE MESSAGE.   
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True,blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()

    is_read = models.BooleanField(default=False, null=True) #IF THE MESSAGE IS JUST SENT, ITS GONNA BE BY DEFAULT FALSE.

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                           primary_key=True, editable=False)

    def __str__(self):
        return self.subject

#ALL THE MESSAGES THAT ARE UNREAD, GONNA BE ON THE TOP OR NEWER CREATED MESSAGES.   
    class Meta:
        ordering = ['is_read', '-created']
    



    
# Signals should be put in some separete file
# go into the user app and create a new file, signals.py 

    
'''  
Instead of writing this, I am using deorator.
def profileUpdated(sender,instance, created, **kwargs):
    print('Profile Saved!')
    print('Instance',instance)
    print('CREATED',created)

def deleteUser(sender, instance, **kwargs):
    print('Deleting User...')
    '''




'''
post_save.connect(profileUpdated, sender=Profile)
post_delete.connect(deleteUser, sender=Profile) '''