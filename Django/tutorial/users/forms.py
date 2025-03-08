from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill


class CustomUserCreationForm(UserCreationForm): # we are inheriting from django user creation form
# So we have all the functionalities like that form

    class Meta:
        model = User
        # What we want to see in the form
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
     # For the signup page, i have deleted the imput div, so it canot be stylled like the login page
     # here i am using this to style the signup page manually without that div.
    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)


        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
         
class profileForm(ModelForm):
    class Meta:
        model  = Profile
        #fields = '__all__'
# Since we don't want all the fiels to be displayed. for this purpose:
        fields = ['name', 'email','location', 'bio', 'short_intro', 'profile_image',
                  'social_github', 'social_linkedin', 'social_twitter', 'social_youtube', 'social_website']
        
    def __init__(self,*args,**kwargs):
        super(profileForm, self).__init__(*args, **kwargs)


        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner'] # this gonna exclude the owner field in SKills Form.
    
    def __init__(self,*args,**kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)


        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})