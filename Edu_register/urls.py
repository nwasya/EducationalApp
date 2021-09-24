from django.urls import path

from Edu_register.views import register_page

urlpatterns = [
    path('register', register_page, name='register'),
]
