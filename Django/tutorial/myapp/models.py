from django.db import models
import uuid
import datetime
from users.models import Profile

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile,null = True, blank=True,
                               on_delete=models.SET_NULL )
    title = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True)
    featured_image = models.ImageField(null=True, blank= True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank= True)
    source_link = models.CharField(max_length=2000, null=True, blank= True)
    tags = models.ManyToManyField('Tag',blank=True)

    vote_total = models.IntegerField(default=0, null=True, blank=True)

    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
#If we want to sort the projects in old first 
#   class Meta:
#        ordering = ['created']

#IF WE WANT TO SORT IT ACCORDING TO HOGHEST VOTE RATIO AND TOTAL.
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def reviewers(self):
#INSTEAD OF GETTING ALL THE ATTRIBUTES OF REVIEWS, WE'RE GETTING THE SINGLE ATTRIBUTE OF REVIEWS.
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset


#THE REVIEWS WE WERE ADDING WERE NOT ACTUALLY UPDATING ON THE FRONTEND.
#TO DO SO, WE ARE WRITING THIS
    @property #SO THAT WE RUN IT AS AN ATTRIBUTE. 
    def getVoteCount(self):
        reviews = self.review_set.all() #GETTING ALL THE REVIEWS
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes /totalVotes ) * 100 
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
    

class Review(models.Model):
    VOTE_TYPE = (
        ('up','Up Vote'),
        ('down','Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # when the model is deleted, all the reviews should also be deleted.
    body = models.TextField(null = True, blank=True)
    value = models.CharField(max_length=200, choices = VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                           primary_key=True, editable=False)

# A USER CAN ONLY LEAVE 1 COMMENT ON THE PROJECT.

    class Meta:
      unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

