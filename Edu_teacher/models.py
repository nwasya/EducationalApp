from django.db import models

# Create your models here.

class TeacherClass(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    role = models.CharField(null=False, max_length=20)
    id_num = models.CharField(max_length=11, null=True)
    phone_number = models.CharField(max_length=12, null=False)

    def __str__(self):
        return self.last_name