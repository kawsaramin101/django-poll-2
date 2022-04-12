from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from ..forms import SignUpForm


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            next_page = request.POST['next'] or "/"
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = HttpResponse()
                response.headers['HX-Redirect'] = next_page
                return response
            else:
                return HttpResponse("Username or Password didn’t match")
        return render(request, 'users/login.html')
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
def logout_view(request):
    logout(request)
    return redirect('/')
    
    
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                response = HttpResponse()
                response.headers['HX-Redirect'] = '/'
                return response
            else:
                return render(request, 'main/partials/signup-form-errors.html', {'errors': form.errors})
        else:
            form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
def check_username_availability(request):
    if request.method == "POST":
        username=request.POST["username"]
        if username == "":
            return HttpResponse("")
        
        user_obj=User.objects.filter(username=username)
        if user_obj.exists():
            return HttpResponse("Username is already taken, please select another one.")
        return HttpResponse("")
    return HttpResponse("Method not allowed")