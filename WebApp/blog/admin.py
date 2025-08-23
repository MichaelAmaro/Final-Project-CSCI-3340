from django.contrib import admin
from .models import Event, RSVP

# Register your models here so they show up in the admin page
admin.site.register(Event)
admin.site.register(RSVP) #  i still need to add the RSVP model to the admin page
