from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from Edu_course.models import Course


class UserProfile(models.Model):
    ROLES = (
        ('Manager', 'Manager'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    )

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES, max_length=20, null=False)
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name


class Student(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    role = models.CharField(null=False, max_length=20)
    id_num = models.CharField(max_length=11, null=True)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    phone_number = models.CharField(max_length=12, null=False)
    is_registered = models.BooleanField(default=False)
    registered_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)


    



    def __str__(self):
        return self.last_name



