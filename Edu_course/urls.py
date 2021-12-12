from django.urls import path

from Edu_book.views import SearchProductsView
from Edu_course.views import course_detail, SearchCoursesView, CourseListAll, CourseListKids, CourseListChildren, \
    CourseListAdults, CourseListTeenAgers, CourseListActives, create_course_page, delete_course_page, edit_course_page

urlpatterns = [
    path('courses/all', CourseListAll.as_view(), name='courses-all'),
    path('courses/kids', CourseListKids.as_view(), name='courses-kids'),
    path('courses/children', CourseListChildren.as_view(), name='courses-children'),
    path('courses/teen-agers', CourseListTeenAgers.as_view(), name='courses-teen-agers'),
    path('courses/adults', CourseListAdults.as_view(), name='courses-adults'),
    path('courses/active-courses', CourseListActives.as_view(), name='courses-active-courses'),
    path('course-detail/<courseId>', course_detail),
    path('addcourse', create_course_page, name='addcourse'),
    path('deletecourse', delete_course_page, name='deletecourse'),
    path('editcourse', edit_course_page, name='editcourse'),


    path('courses/search', SearchCoursesView.as_view()),

]
