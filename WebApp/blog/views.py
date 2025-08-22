from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Event
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

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Event.objects.filter(author=user).order_by('-date_posted')

class EventDetailView(DetailView):
    model = Event
    template_name = 'blog/post_detail.html'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) #running the form on our parent class
    
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False
    
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'
    
    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False

def about(request):
    return render(request, 'blog/Events.html', {'title': 'Events'})






