from django.db import models
from django.utils import timezone #for our date_posted field
from django.contrib.auth.models import User # for our author field

class Post(models.Model): # inheriting from the models.Model class
    title = models.CharField(max_length=200)
    content = models.TextField() 
    date_posted = models.DateTimeField(default=timezone.now)  # this is the date and time the post was created
    author = models.ForeignKey(User, on_delete=models.CASCADE) #cascading means that if the user is deleted then all the posts will be deleted
    
    def __str__(self):
        return self.title
