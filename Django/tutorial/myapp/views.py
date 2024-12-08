from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProjectForm

# Create your views here.
def greeting(request):
    return HttpResponse("Hello Adan!")

def project(request):
    return render(request, 'navbar.html',)

def createProject(request):
    form = ProjectForm()
    context = {'form': form}
    return render(request, "project_form.html", context)