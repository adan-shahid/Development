from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from myapp.models import Project

@api_view(['GET', 'POST'])
def getRoutes(request):
    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    return Response(routes,)

#FOR THE SERIALIZER TO WORK, WE GONNA CREATE OUR VIEW.

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all() # QUERING OUR PROJECT
    serializer = ProjectSerializer(projects, many=True)
#SIMPLY PUTTING THE projects does not work here,we need to put json/serialized data.   
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk) # QUERING OUR PROJECT
    serializer = ProjectSerializer(project, many=False)
#SIMPLY PUTTING THE projects does not work here,we need to put json/serialized data.   
    return Response(serializer.data)