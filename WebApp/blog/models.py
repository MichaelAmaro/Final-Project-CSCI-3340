from django.db import models
from django.utils import timezone #for our date_posted field
from django.contrib.auth.models import User # for our author field
from django.urls import reverse

class Event(models.Model): # inheriting from the models.Model class
    title = models.CharField(max_length=200)
    description = models.TextField() 
    event_date = models.DateField()  # the date when the event will take place
    event_time = models.TimeField()  # the time when the event will start
    location = models.CharField(max_length=200)  # where the event will be held
    date_posted = models.DateTimeField(default=timezone.now)  # this is the date and time the event was created
    author = models.ForeignKey(User, on_delete=models.CASCADE) #cascading means that if the user is deleted then all the events will be deleted
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk}) #full path as a string




