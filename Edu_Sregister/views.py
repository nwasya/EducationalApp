from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from Edu_Mark.models import Mark
from Edu_Sregister.models import RegisteredStudent
from Edu_book.models import Product
from Edu_course.models import Course
from Edu_order.models import OrderDetail
from Edu_user.models import Student, UserProfile
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client

MERCHANT = 'eef9f4c5-a94d-498c-a2d4-75e0bdadbad0'

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'Ehraghi.aysan@gmail.com'  # Optional
mobile = '09337814796'  # Optional

# client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
client = Client('https://zarinpal.com/pg/services/WebGate/wsdl')

# CallbackURLregister = 'http://127.0.0.1:8000/verify_register'
CallbackURLregister = 'http://sahand-esteglal.ir/verify_register'


def verify_new_term_registration(request, *args, **kwargs):
    course_id = kwargs.get('course_id')
    course_obj = Course.objects.get(id=course_id)
    student_id = kwargs.get('student_id')
    student_obj = Student.objects.get(id_num=student_id)

    if request.GET.get('Status') == 'OK':

        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], course_obj.price)
        if result.Status == 100 or result.Status == 101:
            RegisteredStudent(student=student_obj, course=course_obj, price=course_obj.price, time=datetime.now(),
                              rahgiri=result['RefID']).save()
            student_obj.course = course_obj
            student_obj.is_registered = True
            student_obj.save()
            return redirect(f"/payment-success/{result['RefID']}")
        else:
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
            return redirect('/payment-error')
    else:
        return redirect('/payment-error')
        # return HttpResponse('Transaction failed or canceled by user')


def send_request_register(request, *args, **kwargs):
    course_id = kwargs.get('course_id')
    course_obj = Course.objects.get(id=course_id)
    student_id = request.user.username
    result = client.service.PaymentRequest(
        MERCHANT, course_obj.price, description, email, mobile, f"{CallbackURLregister}/{course_id}/{student_id}"
    )
    if result.Status == 100:
        # return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
        return redirect('https://zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


@login_required(login_url='/login')
def new_term_registration(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Student':
        return redirect('/')
    context = {}

    if request.method == "POST":
        course_id = request.POST.get('course_id')

        return redirect(f"/request_regiter/{course_id}")

    current_course = Student.objects.get(id_num=request.user.username).course
    next_course = Course.objects.get(id=current_course.id).next_course

    if next_course is None:
        context['course'] = 'undefined'
    else:
        mark_obj = Mark.objects.filter(student_name__id_num=request.user.username,

                                       course_name=current_course,

                                       ).first()

        if mark_obj is not None:

            total_mark = int(float(mark_obj.total_mark))

        else:

            next_course = 'no-mark'
            total_mark = -1

        if total_mark < 75 and total_mark != -1:
            next_course = 'failed'

        context['course'] = next_course
    print(context)

    return render(request, 'new_termm_registration.html', context)


@login_required(login_url='/login')
def new_term_book_registration(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Student':
        return redirect('/')
    context = {}

    course = Student.objects.get(id_num=request.user.username).course
    course_id_num = course.id_num
    register_date = RegisteredStudent.objects.filter(course=course, student__id_num=request.user.username)
    if register_date.count() == 1:
        register_date = register_date.first().time
        register_date = register_date.replace(tzinfo=None)
        now = datetime.now()
        dd = (now - register_date).days
    else:
        dd = 200

    if dd < 7:

        next_term_books = Product.objects.filter(course__id_num=course_id_num, active=True)
        order_detail = OrderDetail.objects.filter(order__owner__username=request.user.username, is_delivered=True)
    else:
        next_term_books = None
        order_detail = []

    if next_term_books == None:
        context['main_products'] = None
    else:
        minor_books = set(next_term_books.filter(is_main=False))
        main_books = set(next_term_books.filter(is_main=True))
        for order in order_detail:
            if order.product in main_books:
                main_books.remove(order.product)
            elif order.product in minor_books:
                minor_books.remove(order.product)

        context['main_products'] = main_books
        context['minor_products'] = minor_books
        if len(minor_books) == 0 and len(main_books) == 0:
            context['main_products'] = None

        order_detail = OrderDetail.objects.filter(order__owner__username=request.user.username,
                                                  order__is_paid=False)

        li = []
        for i in order_detail:
            li.append(i.product.id_num)
        context['order_cart'] = li

    return render(request, 'new_term_book_registration.html', context)
