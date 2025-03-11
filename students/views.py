from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')


def login(request):
    # this will be the home page...when clicked on the link login field should show
    # in login page no need for base.html,,,jst add same footer and registration page link
    return render(request, 'login.html') 

# def home(request):
#     if request.user.is_authenticated:
#         students = "students"

#     return render(request, 'dashboard.html')
    
    
    #return render(request, 'registration.html')
    


@login_required
def dashboard(request):
    user = request.user
    return render(request, 'index.html')