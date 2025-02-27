from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm): # we are inheriting from django user creation form
# So we have all the functionalities like that form

    class Meta:
        model = User
        # What we want to see in the form
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
         
