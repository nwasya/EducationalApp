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

import requests
import json

from zeep import Client

MERCHANT = 'eef9f4c5-a94d-498c-a2d4-75e0bdadbad0'

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'Ehraghi.aysan@gmail.com'  # Optional
mobile = '09337814796'  # Optional

# client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

# CallbackURLregister = 'http://127.0.0.1:8000/verify_register'
CallbackURLregister = 'http://sahand-esteglal.ir/verify_register'


def verify_new_term_registration(request, *args, **kwargs):
    course_id = kwargs.get('course_id')
    course_obj = Course.objects.get(id=course_id)
    student_id = kwargs.get('student_id')
    student_obj = Student.objects.get(id_num=student_id)
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']

    if request.GET.get('Status') == 'OK':

        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": course_obj.price,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)

        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                RegisteredStudent(student=student_obj, course=course_obj, price=course_obj.price, time=datetime.now(),
                                  rahgiri=req.json()['data']['ref_id']).save()
                student_obj.course = course_obj
                student_obj.is_registered = True
                student_obj.save()
                course_obj.active = True
                course_obj.save()
                x = Product.objects.filter(course=course_obj)
                if x.exists():
                    for item in x:
                        item.active = True
                        item.save()

                return redirect(f"/payment-success/{req.json()['data']['ref_id']}")

            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))

            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
                return redirect('/payment-error')
    else:
        return redirect('/payment-error')


def send_request_register(request, *args, **kwargs):
    course_id = kwargs.get('course_id')
    course_obj = Course.objects.get(id=course_id)
    student_id = request.user.username
    req_data = {
        "merchant_id": MERCHANT,
        "amount": course_obj.price,
        "callback_url": f"{CallbackURLregister}/{course_id}/{student_id}",

        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


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
    context = {'expire': False}

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
        context['expire'] = True
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
