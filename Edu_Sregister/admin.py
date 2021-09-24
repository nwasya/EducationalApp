from django.contrib import admin

# Register your models here.
from Edu_Sregister.models import RegisteredStudent



class StudentRegisterAdmin(admin.ModelAdmin):
    list_display = ['__str__','course','price','time' ]




admin.site.register(RegisteredStudent, StudentRegisterAdmin)