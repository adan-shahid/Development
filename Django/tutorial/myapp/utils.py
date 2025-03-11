from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    # Code for pagination starts here.
    # on one page, it will show 3 projects.
    #page = 1
    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
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

    return custom_range, projects  













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