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

    current_course_id_num = Student.objects.get(id_num=request.user.username).course.id_num
    next_course_id_num = int(current_course_id_num) + 1
    current_course_title = Student.objects.get(id_num=request.user.username).course.title

    course_objects = Course.objects.filter(id_num=current_course_id_num)
    if course_objects.count() > 1:

        if 'girl' in current_course_title or 'دختر' in current_course_title:
            next_course_obj = Course.objects.filter(id_num=next_course_id_num, title__icontains='girl')
            mark_obj = Mark.objects.filter(student_name__id_num=request.user.username,
                                           course_name__id_num=current_course_id_num,
                                           course_name__title__exact=current_course_title).first()
            if mark_obj is not None:
                total_mark = int(float(mark_obj.total_mark))
            else:
                total_mark = 0

            if not next_course_obj.exists() or next_course_obj.count() != 1 or total_mark < 70:
                next_course_obj = None
            else:
                next_course_obj = Course.objects.filter(id_num=next_course_id_num, title__icontains='girl'
                                                        ).first()

            context['course'] = next_course_obj

        elif 'boy' in current_course_title or 'پسر' in current_course_title:

            next_course_obj = Course.objects.filter(id_num=next_course_id_num, title__icontains='boy',
                                                    )

            mark_obj = Mark.objects.filter(student_name__id_num=request.user.username,

                                           course_name__id_num=current_course_id_num,

                                           course_name__title__exact=current_course_title).first()

            if mark_obj is not None:

                total_mark = int(float(mark_obj.total_mark))

            else:

                total_mark = 0

            if not next_course_obj.exists() or next_course_obj.count() != 1 or total_mark < 70:
                next_course_obj = None
            else:

                next_course_obj = Course.objects.filter(id_num=next_course_id_num, title__icontains='boy',
                                                        ).first()
            context['course'] = next_course_obj

        elif 'online' in current_course_title or 'آنلاین' in current_course_title:

            next_course_obj = Course.objects.filter(id_num=next_course_id_num, title__icontains='online',
                                                    )

            mark_obj = Mark.objects.filter(student_name__id_num=request.user.username,

                                           course_name__id_num=current_course_id_num,

                                           course_name__title__exact=current_course_title).first()

            if mark_obj is not None:

                total_mark = int(float(mark_obj.total_mark))

            else:

                total_mark = 0

            if not next_course_obj.exists() or next_course_obj.count() != 1 or total_mark < 70:
                next_course_obj = None
            else:
                next_course_obj = Course.objects.filter(id_num=next_course_id_num, title__icontains='online',
                                                        ).first()
            context['course'] = next_course_obj

    else:

        next_course_obj = Course.objects.filter(id_num=next_course_id_num)
        mark_obj = Mark.objects.filter(student_name__id_num=request.user.username,
                                       course_name__id_num=current_course_id_num).first()
        if mark_obj is not None:
            total_mark = int(float(mark_obj.total_mark))
        else:
            total_mark = 0

        if not next_course_obj.exists() or next_course_obj.count() != 1 or total_mark < 70:
            next_course_obj = None
        else:
            next_course_obj = Course.objects.get(id_num=next_course_id_num)
        context['course'] = next_course_obj

    return render(request, 'new_termm_registration.html', context)


@login_required(login_url='/login')
def new_term_book_registration(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Student':
        return redirect('/')
    context = {}

    next_course_id_num = Student.objects.get(id_num=request.user.username).course.id_num

    next_term_books = Product.objects.filter(course__id_num=next_course_id_num)
    order_detail = OrderDetail.objects.filter(order__owner__username=request.user.username, is_delivered=True)
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

        print(minor_books)
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
