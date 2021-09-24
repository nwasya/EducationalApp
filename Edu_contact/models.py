from django.db import models


# Create your models here.


class ContactUs(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    subject = models.CharField(max_length=200)
    text = models.TextField(max_length=500)
    is_read = models.BooleanField()

    def __str__(self):
        return self.subject
