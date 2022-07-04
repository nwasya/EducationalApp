from django.urls import path

from Edu_account.views import login_page, log_out, registration_detail, user_account, create_books_page, create_student_page, \
    create_teacher_page, ShowContactsInfo, ShowRegistrationRequests, \
    change_password, delete_teacher_page, delete_student_page, \
    delete_book_page, unconfirmedcomments, confirmedcomments, delete_comment, \
    confirm_comment, edit_teacher_page, edit_student_via_modal,edit_course_via_modal, \
    edit_book_page, recent_orders, order_detail, recent_registration, add_online_class_link, transfer_student
from django.contrib.auth.decorators import login_required

from Edu_course.views import edit_course_page, delete_course_page, create_course_page

urlpatterns = [
    path('login', login_page, name='login'),
    path('logout', log_out, name='logout'),
    path('user', user_account, name='user'),
    path('addbook', create_books_page, name='addbooks'),
    path('deletebook', delete_book_page, name='deletebook'),
    path('editbook', edit_book_page, name='editbook'),
    path('addstudent', create_student_page, name='addstudent'),
    path('deletestudent', delete_student_page, name='deletestudent'),
    path('addteacher', create_teacher_page, name='addteacher'),
    path('deleteteacher', delete_teacher_page, name='deleteteacher'),
    path('editteacher', edit_teacher_page, name='editteacher'),
    path('showcontact', login_required(ShowContactsInfo.as_view()), name='showcontact'),
    path('showcomments/<comment_id>', delete_comment),
    path('confirmcomments/<comment_id>',confirm_comment),
    path('showcomments', confirmedcomments,name='showcomments'),
    path('unconfirmedcomments', unconfirmedcomments, name='unconfirmedcomments'),
    path('showregistration', login_required(ShowRegistrationRequests.as_view()), name='showregistration'),
    path('changepassword', change_password, name='change_password'),
    path('recent-orders',  recent_orders, name='recent_orders'),
    path('order-detail',  order_detail, name='order_detail'),
    path('recent_registration', recent_registration, name='recent_registration'),
    path('add_online_class_link', add_online_class_link, name='add_online_class_link'),
    path('transfer-student', transfer_student, name='transfer_student'),
    path('registration_detail', registration_detail, name='registration_detail'),
    path('edit_student_via_modal', edit_student_via_modal, name='edit_student_via_modal'),
    path('edit_course_via_modal', edit_course_via_modal, name='edit_course_via_modal'),
]
