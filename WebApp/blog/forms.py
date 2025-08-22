from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'event_time', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your event...', 'rows': 4}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter event location'}),
        }
        labels = {
            'title': 'Event Title*',
            'description': 'Description*',
            'event_date': 'Event Date*',
            'event_time': 'Event Time*',
            'location': 'Location*',
        }
        help_texts = {
            'event_date': 'Select the date when your event will take place',
            'event_time': 'Select the time when your event will start',
            'location': 'Where will your event be held?',
        }
