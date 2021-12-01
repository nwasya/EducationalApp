from django.db import models

# Create your models here.
from Edu_user.models import Student


class GameCategory(models.Model):
    category = models.CharField(max_length=20)
    categoryurl = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.category


class GameScore(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    category = models.OneToOneField(GameCategory, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, default=0)
    correct_answers = models.IntegerField(null=True, default=0)
    wrong_answers = models.IntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"
