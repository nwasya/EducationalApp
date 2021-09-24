from django.db import models

# Create your models here.
from django.db.models import Q

from Edu_book.models import upload_image_path


class NewsManager(models.Manager):


    def get_news_by_category(self, category_name):
        return self.get_queryset().filter(categories__name__iexact=category_name, active=True)

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None


class News(models.Model):
    title = models.CharField(max_length=150)
    user_name = models.CharField(max_length=100)
    upload_date = models.DateField(auto_now_add=True)
    upload_time = models.TimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    text = models.TextField()
    active = models.BooleanField(default=True)

    # categories = models.ManyToManyField(ProductCategory, blank=True, verbose_name="دسته بندی ها")

    objects = NewsManager()

    def __str__(self):
        return self.title
