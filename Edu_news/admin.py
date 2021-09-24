from django.contrib import admin

# Register your models here.
from Edu_news.models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user_name']


admin.site.register(News, NewsAdmin)
