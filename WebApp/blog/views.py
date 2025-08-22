from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # this is the ordering of the posts by date newest to oldest "-"" means newest to oldest
    paginate_by = 5 # this is the number of posts per page im still deciding to add images or not so depending ill see how big the page will be

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # this is the ordering of the posts by date newest to oldest "-"" means newest to oldest
    paginate_by = 5 # this is the number of posts per page im still deciding to add images or not so depending ill see how big the page will be

    def get_queryset(self): #if user doesnt exsit tell the user that the user doesnt exsit
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) #running the form on our parent class
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/Events.html', {'title': 'Events'})






