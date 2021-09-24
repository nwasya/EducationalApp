from django.contrib import admin

# Register your models here.
from Edu_user.models import UserProfile, Student


class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'role']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'first_name' ,'course']



admin.site.register(Student, StudentAdmin)
admin.site.register(UserProfile, UserAdmin)


