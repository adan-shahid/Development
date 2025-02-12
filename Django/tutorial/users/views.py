from django.shortcuts import render
from .models import Profile, Skill
# Create your views here.

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

