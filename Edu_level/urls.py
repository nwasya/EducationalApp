from django.urls import path

from Edu_book.views import SearchProductsView
from Edu_course.views import course_detail
from Edu_level.views import levels_detail, add_level, edit_level, delete_level

urlpatterns = [

    path('levels-detail/<levelId>/<name>', levels_detail),
    path('add-level', add_level,name='add-level'),
    path('edit-level', edit_level,name='edit-level'),
    path('delete-level', delete_level,name='delete-level')

]
