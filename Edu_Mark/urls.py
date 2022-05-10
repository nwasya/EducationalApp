from django.urls import path

from Edu_Mark.views import enter_mark_page, final_report, view_student_report, edit_mark_page, \
    enter_mark_choose_course_page, enter_mark_choose_student_page, edit_mark_choose_course_page, \
    edit_mark_choose_student_page

urlpatterns = [
    path('add-mark-cc', enter_mark_choose_course_page, name='enter-mark-choose-course'),
    path('add-mark-cs/<course_id>', enter_mark_choose_student_page, name='enter-mark-choose-student'),
    path('add-mark/<course_id>/<student_id>', enter_mark_page, name='enter-mark'),
    path('final-report/<course_id>', final_report, name='final-report'),
    path('view-student-report', view_student_report, name='view_student_report'),
    path('edit-mark-cc', edit_mark_choose_course_page, name='edit-mark-choose-course'),
    path('edit-mark-cs/<course_id>', edit_mark_choose_student_page, name='edit-mark-choose-student'),
    path('edit-mark/<course_id>/<student_id>', edit_mark_page, name='edit-mark'),

]