from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from Edu_comment.models import ProductComment, CourseComment


class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ['full_name','time','confirmed' ]

class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['full_name','time','confirmed' ]


admin.site.register(CourseComment, CourseCommentAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
