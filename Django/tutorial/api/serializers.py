from rest_framework import serializers
from myapp.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project  #THESE 2 LINES GONNA CONVERT THE PROJECT MODEL
        fields = '__all__' # INTO JSON FORM.