from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Event, RSVP
from .forms import EventForm


''' 
this is the old way of doing it, now we are using the Event class so im commenting it out for now later deltet when cleaning it up
# a list of dummy data dictionaries
events = [
    {
        'author': 'Luciana F',
        'title': 'Event 1',
        'description': 'First event description',
        'date_posted': 'August 14, 2025'
    },
    {
        'author': 'Michael A',
        'title': 'Event 2',
        'description': 'Second event description',
        'date_posted': 'August 15, 2025'
    }
]
'''

def home(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'blog/home.html', context)

class EventListView(ListView):
    model = Event
    template_name = 'blog/home.html'
    context_object_name = 'events'
    ordering = ['-date_posted']
    paginate_by = 5

class UserEventListView(ListView):
    model = Event
    template_name = 'blog/user_post.html'
    context_object_name = 'events'
    paginate_by = 5

    def get_queryset(self): # this is the query set for the user event list view
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Event.objects.filter(author=user).order_by('-date_posted')

class EventDetailView(DetailView):
    model = Event
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs): # this is the context data for the event detail view
        context = super().get_context_data(**kwargs)
        context['is_rsvpd'] = self.object.is_user_rsvpd(self.request.user)
        context['rsvp_count'] = self.object.rsvp_count()
        return context

class EventCreateView(LoginRequiredMixin, CreateView): # this is the view for the event create view
    model = Event
    form_class = EventForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form): # this is the form valid for the event create view
        form.instance.author = self.request.user
        return super().form_valid(form) #running the form on our parent class
    
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # this is the view for the event update view
    model = Event
    form_class = EventForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form): # this is the form valid for the event update view
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self): # this is the test function for the event update view
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False
    
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # this is the view for the event delete view
    model = Event
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'
    
    def test_func(self): # this is the test function for the event delete view
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False

@login_required
def toggle_rsvp(request, event_id): # this is the view for the  rsvp view
    """Toggle RSVP status for an event"""
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    
    # Check if user already RSVP'd
    rsvp, created = RSVP.objects.get_or_create(user=user, event=event)
    
    if not created:
        # User already RSVP'd, so remove it
        rsvp.delete()
        messages.success(request, f'You have cancelled your RSVP to {event.title}')
        is_rsvpd = False
    else:
        # User just RSVP'd
        messages.success(request, f'You have RSVP\'d to {event.title}!')
        is_rsvpd = True
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_rsvpd': is_rsvpd,
            'rsvp_count': event.rsvp_count()
        })
    
    return redirect('event-detail', pk=event_id)

@login_required
def my_events(request): # this is the view for the my events view
    """Show events that the current user has RSVP'd to"""
    user_rsvps = RSVP.objects.filter(user=request.user).select_related('event').order_by('event__event_date')
    events = [rsvp.event for rsvp in user_rsvps]
    
    context = {
        'events': events,
        'title': 'My Events'
    }
    return render(request, 'blog/my_events.html', context)

def about(request): # this is the view for the about view
    return render(request, 'blog/Events.html', {'title': 'Events'})






