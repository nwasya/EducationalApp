from django.contrib import admin

# Register your models here.
from Edu_course.models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ['__str__','id_num','active','teacher' ]




admin.site.register(Course, CourseAdmin)
