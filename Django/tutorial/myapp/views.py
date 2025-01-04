from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import Project


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
    projects = Project.objects.all()
    context = {'projects':projects}
    # context = {'page':page, 'age':age, 'projects':projectsList}
    return render(request,'index.html', context)

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    # for i in  projectsList:
    #     if i['id'] == pk:
    #         projectObj = i
    return render(request, 'single-project.html', {'project': projectObj}) #'tags':tags })

def createform(request):
    return render(request, 'project_form.html')