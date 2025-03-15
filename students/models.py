from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    course_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    password = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
