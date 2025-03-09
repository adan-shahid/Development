from .models import Project, Tag
from django.db.models import Q

def searchProject(request):
    text = ''
    if request.GET.get('text'):
        text = request.GET.get('text')

    tags = Tag.objects.filter(name__icontains=text)


    #projects = Project.objects.all()
    projects = Project.objects.distinct().filter(Q(title__icontains=text) |
                                      Q(description__icontains=text) |
                                      Q(owner__name__icontains=text) |
                                      Q(tags__in=tags)
                                      )

    return projects, text