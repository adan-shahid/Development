from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

#@receiver(post_save,  sender=Profile)    
def createdProfile(sender, instance, created, **kwargs ):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email= user.email,
            name=user.first_name,
        )

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete() 
   

post_save.connect(createdProfile, sender=User) #anytime a user model will be created, details will be shown.
post_delete.connect(deleteUser, sender=Profile)

# Now Do we tell the django that signals are here?
    # Check inside apps.py

