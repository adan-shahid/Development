from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag 

# In order to see the model in the django admin panel.
# We need to register here.

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)

