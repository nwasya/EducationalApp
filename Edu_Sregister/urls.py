from django.urls import path

from Edu_Sregister.views import verify_new_term_registration, send_request_register, new_term_registration, \
    new_term_book_registration

urlpatterns = [

    path('verify_register/<course_id>/<student_id>', verify_new_term_registration, name='verify_register'),
    path('request_regiter/<course_id>', send_request_register, name='request_register'),
    path('new_term_register', new_term_registration, name='new_term_registration'),
    path('new_term_book_registration', new_term_book_registration, name='new_term_book_registration'),
]