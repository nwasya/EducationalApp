import os

from django.db import models

from django.db.models import Q
from Edu_course.models import Course



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

class ProductsManager(models.Manager):
    def get_active_products(self):
        x = self.get_queryset().filter(active=True).reverse()
        return x


    def get_main_products(self):
        x = self.get_queryset().filter(is_main=True).reverse()
        return x

    def get_products_by_category(self, category_name):
        return self.get_queryset().filter(categories__name__iexact=category_name, active=True)

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
        return self.get_queryset().filter(lookup, active=True).distinct()

    #Q(tag__title__icontains=query) in bayad bala copy she


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    active = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    id_num = models.IntegerField()
    course = models.ManyToManyField(Course)

    objects = ProductsManager()



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/products/{self.id}/{self.title.replace(' ', '-')}"

# class ProductGallery(models.Model):
#     title = models.CharField(max_length=150, verbose_name='عنوان')
#     image = models.ImageField(upload_to=upload_gallery_image_path, verbose_name='تصویر')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
#
#     class Meta:
#         verbose_name = 'تصویر'
#         verbose_name_plural = 'تصاویر'
#
#     def __str__(self):
#         return self.title
