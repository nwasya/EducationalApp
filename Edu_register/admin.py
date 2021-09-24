from django.contrib import admin
from Edu_register.models import Register
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ['full_name','phone','birth','is_read']
    list_filter = ['is_read']
    list_editable = ['is_read']
    search_fields = ['description','full_name','latest_course']


admin.site.register(Register,RegisterAdmin)

