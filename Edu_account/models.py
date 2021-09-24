from django.db import models

# Create your models here.


class PassReset(models.Model):
    password_new = models.CharField(max_length=20)
    re_password_new = models.CharField(max_length=20)