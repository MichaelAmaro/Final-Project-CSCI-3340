from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid(): # when the form is valid, we save the user
            form.save() # this is the line that saves the userrrrrrrr
            username = form.cleaned_data.get('username') 
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login') # they will go to the login page
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form}) # this is the template that we will use to display the form

@login_required  # this is the decorator that will prevent users from accessing the profile page if they are not logged in
def profile(request):
    return render(request, 'users/profile.html')


'''
# this is the different types of messages that can be displayed
messages.debug
messages.info
messages.success
messages.warning
messages.error
'''