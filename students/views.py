from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student, Course
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404
from django.contrib.auth.decorators import login_required

# Create your views here.


# User Login

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the user is an admin (User model)
        
        user = User.objects.filter(email=email).first()
        if user:
            user = authenticate(request, username=user.username, password=password)
            if user:
                auth_login(request, user)
                return redirect('dashboard')
                

        # Check if the user is a student (Student model)
        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):  # Validate hashed password
                request.session['student_id'] = student.id  # Store student ID in session
                return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except Student.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')


# Student Registration
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        course_id = request.POST.get("course")
        course_fee = request.POST.get("course_fee")
        password = request.POST.get("password")

        if Student.objects.filter(email=email).exists():
            messages.error(request, "This Email is already registered")
            return redirect('register')
        
         # Hash the password before saving
        hashed_password = make_password(password)

        course = Course.objects.get(id=course_id) if Course.objects.filter(id=course_id).exists() else None

         # Auto-assign course fee if not provided
        if not course_fee and course:
            course_fee = course.fee

        student = Student.objects.create(
            name=name,
            email=email,
            phone_no=phone_no,
            course=course,
            course_fee=course_fee if course_fee else 0,
            password=hashed_password 
        )

        messages.success(request, "Registration is successful. You can now log in.")
        return redirect('login')

    context = {
        "courses": Course.objects.all()
        }
    return render(request, 'registration.html', context)




# student list from Admin user
@login_required
def dashboard(request):
    if not request.user.is_staff:  # Allow only admin users
        messages.error(request, "Unauthorized access")
        return redirect('login')
    
    messages.success(request, " Login Successful.")

    context = {"students": Student.objects.all().order_by("-created_at")}
    
    return render(request, 'index.html', context)


# Student dashboard from student login

def student_dashboard(request):
    # Get the student ID from the session
    student_id = request.session.get('student_id')
    
    if not student_id:
        return redirect('student_login')  # Redirect to login if the student is not logged in

    try:
        student = Student.objects.get(id=student_id)  # Retrieve the student by ID
        course = student.course  # Fetch the course the student is enrolled in (one course)
        
    except Student.DoesNotExist:
        raise Http404("Student not found")
    
    messages.success(request, "Successful Login.")

    context = {
        'student': student,
        'course': course,
    }
    
    return render(request, 'student_dashboard.html', context)
