"""EducationalApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Edu_book.views import product_detail
from Edu_course.views import course_detail
from EducationalApp import settings
from EducationalApp.views import home_page, header, footer, about_designer, about_us, payment_error, \
    payment_success


def connect_to(args):
    pass


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about_designer',about_designer, name='about_designer'),

    path('header', header, name="header"),
    path('footer', footer, name="footer"),
    path('course-detail/<courseId>/<name>', course_detail),
    path('products/<productId>/<name>', product_detail,name='product_detail'),
    path('about-us', about_us,name='about-us'),

    path('payment-success/<serial_num>', payment_success,name='payment_success'),
    path('payment-error', payment_error,name='payment_error'),
    # path('test', test,name='payment_error'),
    #

    path('', include('Edu_account.urls')),
    path('', include('Edu_register.urls')),
    path('', include('Edu_book.urls')),
    path('', include('Edu_contact.urls')),
    path('', include('Edu_course.urls')),
    path('', include('Edu_news.urls')),
    path('', include('Edu_Mark.urls')),
    path('', include('Edu_order.urls')),
    path('', include('Edu_level.urls')),
    path('', include('Edu_Sregister.urls')),
    path('', include('Edu_game.urls')),



]

handler404 = 'EducationalApp.views.handler_404_error'
if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
