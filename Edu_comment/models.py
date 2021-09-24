from django.db import models

# Create your models here.
from django.http import Http404

from Edu_book.models import Product
from Edu_course.models import Course


class ProductCommentManager(models.Manager):
    def get_active_comments(self):
        return self.get_queryset().filter(confirmed=True)
    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def set_status_comment(self, product_id):
        qs = self.get(id=product_id)
        if qs.confirmed:
            qs.confirmed = False
            qs.save()

        else:
            qs.confirmed = True
            qs.save()







class ProductComment(models.Model):
    full_name = models.CharField(max_length=100,null=False)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    text = models.TextField(null=False)
    email = models.EmailField(null=False)
    object = models.ForeignKey(Product,on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    objects = ProductCommentManager()


class CourseComment(models.Model):
    full_name = models.CharField(max_length=100,null=False)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    text = models.TextField(null=False)
    email = models.EmailField(null=False)
    object = models.ForeignKey(Course, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    objects = ProductCommentManager()