from django.http import Http404
from django.shortcuts import render, redirect

from Edu_Sregister.models import RegisteredStudent
from Edu_album.models import AlbumTeacher, AlbumAdult, AlbumTeenage, AlbumInstitute, AlbumChildren
from Edu_book.models import Product
from Edu_book.views import my_grouper

from Edu_course.models import Course
from Edu_level.models import Level
from Edu_order.models import Order
from Edu_teacher.models import TeacherClass
from Edu_user.models import Student, UserProfile


def header(request, *args, **kwargs):
    context = {

    }

    if request.user.is_authenticated:
        user_id = request.user.username
        user_profile = UserProfile.objects.get(user__username=user_id)
        if user_profile.role == 'Student':
            student_obj = Student.objects.get(id_num=user_id)
            course_name = student_obj.course
            course_id = student_obj.course.id
            course_link = Course.objects.get(title__exact=course_name).online_class_link
            context['course_link'] = course_link
            context['course_name'] = course_name
            context['course_id'] = course_id
            context['student'] = True



        elif user_profile.role == 'Teacher':
            pass
        else:
            pass

    return render(request, 'shared/Header.html', context)


def about_designer(request):
    context = {

    }
    return render(request, 'about_me.html', context)


# footer code behind
def footer(request, *args, **kwargs):
    context = {

    }
    return render(request, 'shared/Footer.html', context)


def about_us(request):
    context = {

    }
    return render(request, 'about_us.html', context)


def home_page(request, *args, **kwargs):
    print('okkkkkkkkkk')
    available_courses = Course.objects.get_active_courses().order_by('-id')

    available_products = Product.objects.get_main_products().distinct()

    available_levels = Level.objects.all()
    teachers = TeacherClass.objects.filter(role__exact='Teacher')

    context = {

        'products': available_products,
        'courses': available_courses,
        'levels': available_levels,
        'teachers': teachers

    }

    return render(request, 'home_page.html', context)


def handler_404_error(request, exception):
    return render(request, '404-not-found-page.html', {})


def payment_success(request, *args, **kwargs):
    if request.method == "GET":

        data = kwargs['serial_num']

    else:

        data = None

    return render(request, 'payment_success.html', {"data": data})


def payment_error(request):
    return render(request, 'payment_error.html', {})


# def test(request):
#     return render(request,'test.html',{})
