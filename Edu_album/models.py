from django.db import models

# Create your models here.


from Edu_book.models import upload_image_path


class AlbumTeacher(models.Model):
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    title = models.CharField(max_length=150)
    description = models.TextField(null=False)


class AlbumAdult(models.Model):
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    title = models.CharField(max_length=150)
    description = models.TextField(null=False)


class AlbumTeenage(models.Model):
    image  = models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    title = models.CharField(max_length=150)
    description = models.TextField(null=False)


class AlbumChildren(models.Model):
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    title = models.CharField(max_length=150)
    description = models.TextField(null=False)


class AlbumInstitute(models.Model):
    image  = models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    title = models.CharField(max_length=150)
    description = models.TextField(null=False)