from django.db import models

# Create your models here.
from Edu_course.models import Course
from Edu_user.models import Student


class RegisteredStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    time = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    price = models.IntegerField()
    rahgiri = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'
