from django.db import models

# Create your models here.
from Edu_course.models import Course
from Edu_teacher.models import TeacherClass
from Edu_user.models import Student


class Mark(models.Model):
    RESULT = (
        ('Out_Standing', 'Out Standig'),
        ('Good', 'Good'),
        ('Satisfactory', 'Satisfactory'),
        ('Weak', 'Weak'),
    )
    student_name = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    course_name = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    class_activity = models.CharField(max_length=5)
    quizzes = models.CharField(max_length=5)
    final = models.CharField(max_length=5)
    midterm = models.CharField(max_length=5)
    extra_mark = models.CharField(max_length=5, default=0)
    total_mark = models.CharField(max_length=15)
    total_work = models.CharField(max_length=15, choices=RESULT)
    homework = models.CharField(max_length=15, choices=RESULT,default='Out_Standing')
    writing = models.CharField(max_length=15, choices=RESULT,default='Out_Standing')
    listening = models.CharField(max_length=15, choices=RESULT,default='Out_Standing')
    speaking = models.CharField(max_length=15, choices=RESULT,default='Out_Standing')
    activity = models.CharField(max_length=15, choices=RESULT,default='Out_Standing')
    description = models.TextField(max_length=500,null=True)
    teacher = models.ForeignKey(TeacherClass, on_delete=models.SET_NULL, null=True)


    class Meta:
        unique_together = ('student_name', 'course_name',)
