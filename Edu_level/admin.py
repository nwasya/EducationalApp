from django.contrib import admin

# Register your models here.
from Edu_level.models import Level


class LevelAdmin(admin.ModelAdmin):
    list_display = ['title' ]




admin.site.register(Level, LevelAdmin)
