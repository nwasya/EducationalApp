from django.contrib import admin

# Register your models here.
from Edu_book.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id_num','is_main']




admin.site.register(Product, ProductAdmin)
