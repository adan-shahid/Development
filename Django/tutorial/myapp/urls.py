from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.projects, name="projects"),
    path('project/<str:pk>', views.project, name='project'),
    path('create_form/',views.createForm,name='create_form'),
    path('update-form/<str:pk>', views.updateProject, name='update-form'),
    path('delete-form/<str:pk>', views.deleteProject, name='delete-form'),
    
]