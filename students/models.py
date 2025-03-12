from django.db import models

# Create your models here.
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    phone_no = models.CharField(max_length=15)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)  # ForeignKey to Course model
    course_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional fee, will auto-populate from the course
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name