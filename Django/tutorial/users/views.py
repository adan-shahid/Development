from django.shortcuts import render, redirect
from django.contrib.auth import  login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Profile, Skill
from .forms import CustomUserCreationForm, profileForm



# Create your views here.

def loginUser(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('profiles') 


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #print(request.POST)
        # We want to run a few checks if  a user has send something wrong
        try:
            user = User.objects.get(username=username)
        except:
            #print('Username does not exist')
            messages.error(request,'Username does not exist')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request,'Username or password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request,'Username was logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    # Now we are going to register a user through this form
     
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # here we are creating a temp user form, before storing it.
            user.username = user.username.lower() # to make sure that 2 user not have same username. i.e, lower and capital
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            #return redirect('profiles')
            return redirect('edit-account')
        else:
             messages.success(request, 'An error has occurred during registration')



    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html',context)


def profiles(request):
    profiles = Profile.objects.all()
    skills = Skill.objects.all()
    context = {'profiles':profiles,
               'skills':skills}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id = pk)

    topSkills = profile.skill_set.exclude(description__exact="")

    otherSkills = profile.skill_set.filter(description="")


    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

#@login_required(login_url='login')
#def userAccount(request):
    profile = request.user.profile

    skills = profile.skill.set.all()
    projects = profile.project.set.all()

    context = {'profile':profile, 'skills':skills, 'projects':projects}

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile # If you are not logged in, you will not be able to open this page.
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
  
    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login') # this is decorator
def editAccount(request):

    profile = request.user.profile # we just gonna edit the logged in user.
    form = profileForm(instance=profile) # instance = profile, because we need to prefill those fields.  

    if request.method == 'POST':
        form = profileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

