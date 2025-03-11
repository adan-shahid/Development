
# we gonna write all the search code here, which i wrote in profiles view.
# in order to avoid mess in that view.
# 
from .models import Profile, Skill
from django.db.models import Q 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):
    # Code for pagination starts here.
    # on one page, it will show 3 projects.
    #page = 1
    page = request.GET.get('page')
 #   results = 3, because we are passing this value in our view.
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
# pagination code ends here.
# What if we have 1000 of projects and 100 of buttons show in the pagination. That's not look good.
# so we want to limit the number of buttons on the page. for this we write our own custom class.
# Here this code will show option of 5 pages.
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex,rightIndex)

    return custom_range, profiles  


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