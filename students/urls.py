
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login , name="login"),
    path("register/", views.register , name="register"),
    path("dashboard/", views.dashboard , name="dashboard"),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

]
