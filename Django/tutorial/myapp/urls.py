from django.urls import path
from . import views

urlpatterns = [
    path('', views.greeting, name="greeting" ),
    path('index', views.project, name='project'),
]