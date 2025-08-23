from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, UserEventListView, toggle_rsvp, my_events
from . import views


urlpatterns = [ 
    path('', EventListView.as_view(), name='blog-home'), 
    path('user/<str:username>/', UserEventListView.as_view(), name='user-events'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/new/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('event/<int:event_id>/rsvp/', toggle_rsvp, name='toggle-rsvp'),
    path('my-events/', my_events, name='my-events'),
    path('Events/', views.about, name='blog-Events'),
]

