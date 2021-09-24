from django.contrib import admin


from Edu_Mark.models import Mark



class MarkAdmin(admin.ModelAdmin):
    list_display = ['student_name','course_name','total_mark' ]




admin.site.register(Mark,MarkAdmin)