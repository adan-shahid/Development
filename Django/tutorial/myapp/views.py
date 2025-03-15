from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime

from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProject, paginateProjects

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

# We have a list in which we have 3 Dictionaries.
# projectsList = [
#     {
#         'id':'1',
#         'title':'Ecommerce Website',
#         'description':'Fully Functional Ecommerce Website.'
#     },
#     {
#         'id':'2',
#         'title':'Portfolio Website',
#         'description':'This was a project where I built out my Portfolio'
#     },
#     {
#         'id':'3',
#         'title':'Social Network',
#         'description':'Awesome open source project I am still working'
#     },
# ]

def hello(request):
    day = datetime.datetime.now().date()
    return render(request, 'single-project.html',{'today':day})

def projects(request):

    # page = 'project'
    # age = 10
    projects, text = searchProject(request)

    custom_range, projects = paginateProjects(request, projects, 3)


# because the views becomes messy wo we are moving this code
# to utils.py file

# Code for pagination starts here.
    # on one page, it will show 3 projects.
    #page = 1
#    page = request.GET.get('page')
#    results = 3
#    paginator = Paginator(projects, results)


#    try:
#        projects = paginator.page(page)
#    except PageNotAnInteger:
#        page = 1
#        projects = paginator.page(page)
#    except EmptyPage:
#        page = paginator.num_pages
#       projects = paginator.page(page)
# pagination code ends here.

# What if we have 1000 of projects and 100 of buttons show in the pagination. That's not look good.
# so we want to limit the number of buttons on the page. for this we write our own custom class.
# Here this code will show option of 5 pages.
#   leftIndex = (int(page) - 4)
#    if leftIndex < 1:
#        leftIndex = 1
#    rightIndex = (int(page) + 5)
#   if rightIndex > paginator.num_pages:
#        rightIndex = paginator.num_pages + 1

#    custom_range = range(leftIndex,rightIndex) """



   # we are passing here 'projects', so that it stays in the search bar
    context = {'projects':projects, 'text':text,
              'custom_range':custom_range}
        
    # context = {'page':page, 'age':age, 'projects':projectsList}
    return render(request,'index.html', context)

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    # tags = projectObj.tags.all()
    # for i in  projectsList:
    #     if i['id'] == pk:
    #         projectObj = i
    return render(request, 'single-project.html', {'project': projectObj,'form': form}) #'tags':tags })


# Now someone can only edit these pages, if he is an autheticated user

@login_required(login_url='login') # if the user is not logged in, send him to this page.
def createForm(request):
    profile = request.user.profile # we took the logged in user
    form = ProjectForm()

    if request.method == 'POST':
        
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():

            project = form.save(commit=False) # updated the project 
            project.owner = profile
            project.save()
            return redirect("account")
    context = {'form':form} 
    return render(request,'project_form.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")
    context = {'form':form} 
    return render(request,'project_form.html',context)

@login_required(login_url='login')
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
        
    context = {'object':project}
    return render(request, 'delete_template.html',context)