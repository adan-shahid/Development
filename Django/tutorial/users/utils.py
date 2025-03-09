
# we gonna write all the search code here, which i wrote in profiles view.
# in order to avoid mess in that view.
# 
from .models import Profile, Skill
from django.db.models import Q 

def searchProfiles(request):
    text = ''
    if request.GET.get('text'):
        text = request.GET.get('text')

    skills = Skill.objects.filter(name__icontains= text) # we querying the skills
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
    profiles = Profile.objects.distinct().filter(Q(name__icontains=text) |
                                                 Q(short_intro__icontains=text) | 
                                                 Q(skill__in= skills))
    return profiles, text