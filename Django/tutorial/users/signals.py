from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings

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

        subject = 'Welcome to Dev Search.'
        message = 'We are glad you are here.'

#I WANNA SEND THE EMAIL ONLY WHEN THE USER IS CREATED.
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )





# Now simply we modify the user(in admin) anytime the profile is updated.
# We are doing this to ensure that when a user on website changes its information,
# that changes will also be reflected in the admin portal.

def updateUser(sender, instance, created, **kwargs):
    profile = instance 
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
         

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete() 
   

post_save.connect(createdProfile, sender=User) #anytime a user model will be created, details will be shown.
post_save.connect(updateUser, sender=Profile) # anytime profile is changed, we gonna trigger this view.
post_delete.connect(deleteUser, sender=Profile)

# Now Do we tell the django that signals are here?
    # Check inside apps.py

