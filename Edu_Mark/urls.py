from django.urls import path

from Edu_Mark.views import enter_mark_page, final_report, view_student_report, edit_mark_page

urlpatterns = [
    path('add-mark', enter_mark_page, name='enter-mark'),
    path('final-report', final_report, name='final-report'),
    path('view-student-report', view_student_report, name='view_student_report'),
    path('edit-mark', edit_mark_page, name='edit_mark'),

]