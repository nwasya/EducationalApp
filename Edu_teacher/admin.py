from django.contrib import admin

# Register your models here.
from Edu_teacher.models import TeacherClass


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id_num']


admin.site.register(TeacherClass, TeacherAdmin)