import os

from django.db import models

from django.db.models import Q

from Edu_teacher.models import TeacherClass


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/{final_name}"


def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/galleries/{final_name}"


# Create your models here.

class CourseManager(models.Manager):
    def get_active_courses(self):
        return self.get_queryset().filter(active=True)

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def get_by_id_num(self, product_id):
        qs = self.get_queryset().filter(id_num=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def search(self, query):
        lookup = (
            Q(title__icontains=query)

        )
        return self.get_queryset().filter(lookup).distinct()

    def search_adults(self, query1, query2):

        lookup = (
                Q(title__icontains=query1) |
                Q(title__icontains=query2)

        )
        return self.get_queryset().filter(lookup).distinct()


class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    id_num = models.IntegerField(null=True, default=000)
    price = models.IntegerField()
    teacher = models.ForeignKey(TeacherClass, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    active = models.BooleanField(default=True)
    starting_date = models.CharField(null=False, max_length=10)
    online_class_link = models.CharField(max_length=500, null=True)
    next_course = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    objects = CourseManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/course-detail/{self.id}"
