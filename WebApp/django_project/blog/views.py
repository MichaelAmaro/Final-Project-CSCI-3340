from django.shortcuts import render
from .models import Post #from the models.py file we imported the Post class


''' 
this is the old way of doing it, now we are using the Post class so im commenting it out for now later deltet when cleaning it up
# a list of dummy data dictionaries
posts = [
    {
        'author': 'Luciana F',
        'title': 'Post 1',
        'content': 'First post content',
        'date_posted': 'August 14, 2025'
    },
    {
        'author': 'Michael A',
        'title': 'Post 2',
        'content': 'Second post content',
        'date_posted': 'August 15, 2025'
    }
]
'''

def home(request):
    context = {
        'posts': Post.objects.all()  
    }
    return render(request, 'blog/home.html', context) # this is the template that we will use to display the posts

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})





