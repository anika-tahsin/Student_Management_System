from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Student, Course

from django.contrib.auth.decorators import login_required

# Create your views here.

# User Login

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username= email, password = password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        
        else:
            messages.error(request,"Invalid user or password")

    return render(request, 'login.html') 


# Student Registration
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        course = request.POST.get("course")
        course_fee = request.POST.get("course_fee")
        password = request.POST.get("password")
       
        # check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "This Email is already registered")
            return redirect('register')
        
        # Create new user
        user = User.objects.create_user(username=email, password=password, first_name =name)
        user.save()



        # Link the course using the selected course ID
        course = Course.objects.get(id=course_id)

        # Create the student record
        student = Student.objects.create(
            name=name,
            email=email,
            phone_no=phone_no,
            course=course,
            course_fee=course_fee,
            password=password
        )
        student.save()

        messages.success(request, "Registration is successful. You now can login")
        return redirect('login')

    # Get all courses from the database and pass to the template
    courses = Course.objects.all()

    return render(request, 'registration.html', {'courses': courses})



@login_required
def dashboard(request):
    user = request.user
    return render(request, 'index.html')