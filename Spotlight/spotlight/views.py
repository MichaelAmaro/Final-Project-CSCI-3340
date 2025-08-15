from django.shortcuts import render, redirect


def signin(request): 
    sign_in = signin.objects.all()
    return render(request, 'signin.html', {'signin': signin})
