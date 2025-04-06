from django.shortcuts import render, redirect
from django.contrib.auth import  login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, profileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles



# Create your views here.

def loginUser(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('profiles') 


    if request.method == 'POST':
        username = request.POST['username'].lower()
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        

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


    #text = ''
    #if request.GET.get('text'):
    #    text = request.GET.get('text')

    #skills = Skill.objects.filter(name__icontains= text) # we querying the skills
    #print('Search :', text)

                                #name is the attribute we defined in model.
    #profiles = Profile.objects.filter(name__icontains=text),short_intro__icontains=text) # icontains-->bcz we dont want searching to be case sensitive.

# we cannot write short_intro__icontains=text, because if searched no. is not present in both, then
# no result appears. Here it basically doing AND of name and short_intro.we don't wanna do that.
# as an alternative we import Q.

    #profiles = Profile.objects.filter(Q(name__icontains=text) | 
    #                                  Q(short_intro__icontains=text) | 
    #                                 Q(skill__in= skills)) #does the profile has a skill that is listed in 'skills' query set.

# here we were getting multiple instances of each user. so to avoid that we use distinct().
    #profiles = Profile.objects.distinct().filter(Q(name__icontains=text) | 
    #                                  Q(short_intro__icontains=text) | 
    #                                  Q(skill__in= skills))

    profiles, text = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)

    #profiles = Profile.objects.all()
   # skills = Skill.objects.all()
    context = {'profiles':profiles,
               'text':text,
               'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

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

@login_required(login_url='login') # this is decorator, only logged in user can edit this.
def createSkill(request):

# we also want to associate the skill with the particular owner.

    profile = request.user.profile # associated.
    form = SkillForm()

# Now we gonna process the form.

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid(): # make sure all the data is valid.
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill was added successfully!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login') # this is decorator, only logged in user can edit this.
def updateSkill(request, pk):

# we also want to associate the skill with the particular owner.

    profile = request.user.profile # associated.
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance = skill)

# Now we gonna process the form.
#  
    if request.method == 'POST':
        form = SkillForm(request.POST, instance = skill)
        if form.is_valid(): # make sure all the data is valid.
            # we already know who the owner is.
            form.save()
            messages.success(request,'Skill was Updated successfully!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill was deleted successfully!')
        return redirect('account')
    context = {'object':skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile #1ST GET THE LOGGED IN USER.
#BCZ WE WROTE RELATED_NAME - MESSAGES IN RECIPIENT OBJECT IN MODELS.
    messageRequest = profile.messages.all() 
    unreadCount = messageRequest.filter(is_read=False).count()
    
    context = {'messageRequest':messageRequest, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):

    profile = request.user.profile #1ST GET THE LOGGED IN USER.

#BCZ WE WROTE RELATED_NAME - MESSAGES IN RECIPIENT OBJECT IN MODELS.
    message = profile.messages.get(id=pk) 

#WHENEVER THE USER OPENS THE MESSAGE, IT MARKS AS READ
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'users/message.html', context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

# NOW GONNA WRITE THE LOGIC TO PROCESS THE FORM.
    try: # 1ST WE GONNA GET THE USER.
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)


    context = {'recipient':recipient,'form':form}
    return render(request, 'users/message_form.html', context)


