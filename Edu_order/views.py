import random
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
import time
# Create your views here.
from Edu_course.models import Course
from Edu_order.forms import UserNewOrderForm
from Edu_order.models import Order, OrderDetail
from Edu_book.models import Product

from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client

from Edu_user.models import Student


@login_required(login_url='/login')
def add_user_order(request):
    new_order_form = UserNewOrderForm(request.POST or None)

    if new_order_form.is_valid():
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if order is None:
            order = Order.objects.create(owner_id=request.user.id, is_paid=False)

        product_id = new_order_form.cleaned_data.get('product_id')
        count = new_order_form.cleaned_data.get('count')

        if count < 0:
            count = 1

        product = Product.objects.get_by_id(product_id=product_id)
        order.orderdetail_set.create(product_id=product.id, price=product.price, count=count)
        # todo: redirect user to user panel
        # return redirect('/user/orders')

        return redirect(f'/products/{product.id}/{product.title.replace(" ", "-")}')

    return redirect('/')


@login_required(login_url='/login')
def user_open_order(request):
    context = {
        'order': None,
        'details': None,
        'total': 0
    }

    open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if open_order is not None:
        context['order'] = open_order
        context['details'] = open_order.orderdetail_set.all()
        context['total'] = open_order.get_total_price()

    return render(request, 'order/user_open_order.html', context)


@login_required(login_url='/login')
def remove_order_detail(request, *args, **kwargs):
    detail_id = kwargs.get('detail_id')
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get(id=detail_id, order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()
            return redirect('/open-order')
    raise Http404()


@login_required(login_url='/login')
def remove_order_detail_via_new_term_regitration(request, *args, **kwargs):
    detail_id = kwargs.get('ProductId')
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().filter(product__id_num=detail_id,
                                                                 order__owner_id=request.user.id, order__is_paid=False)
        if order_detail is not None:
            order_detail.delete()
            return redirect('/new_term_book_registration')
    raise Http404()


MERCHANT = 'eef9f4c5-a94d-498c-a2d4-75e0bdadbad0'

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'Ehraghi.aysan@gmail.com'  # Optional
mobile = '09337814796'  # Optional

# client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
client = Client('https://zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://127.0.0.1:8000/verify'
# CallbackURL = 'http://sahand-esteglal.ir/verify'



#
# Important: need to edit for realy server.


def send_request(request, *args, **kwargs):
    total_price = 0
    open_order: Order = Order.objects.filter(is_paid=False, owner_id=request.user.id).first()
    if open_order is not None:
        total_price = open_order.get_total_price()
        result = client.service.PaymentRequest(
            MERCHANT, total_price, description, email, mobile, f"{CallbackURL}/{open_order.id}"
        )
        if result.Status == 100:
            return redirect('https://zarinpal.com/pg/StartPay/' + str(result.Authority))
            # return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))
    raise Http404()


def verify(request, *args, **kwargs):
    order_id = kwargs.get('order_id')
    order = Order.objects.filter(is_paid=False, owner_id=request.user.id).first()
    # if order is not None:
    if request.GET.get('Status') == 'OK':

        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], order.get_total_price())
        if result.Status == 100:
            order_detail = OrderDetail.objects.filter(order__owner__username=request.user.username, is_delivered=False)
            for order in order_detail:
                order.is_delivered = True
                order.save()

            user_order = Order.objects.get_queryset().get(id=order_id)
            user_order.is_paid = True
            user_order.payment_date = datetime.now()
            user_order.seril_num = result['RefID']
            user_order.total_price = user_order.get_total_price()
            user_order.save()

            return redirect(f"/payment-success/{result['RefID']}")

            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        # elif result.Status == 101:
        #     return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return redirect('/payment-error')
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return redirect('/payment-error')
        # return HttpResponse('Transaction failed or canceled by user')




@login_required(login_url='/login')
def add_user_order_via_link(request, *args, **kwargs):
    order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if order is None:
        order = Order.objects.create(owner_id=request.user.id, is_paid=False, total_price=0)

    product_id = kwargs['productId']
    count = 1
    product = Product.objects.filter(id_num=product_id).first()

    order.orderdetail_set.create(product=product, price=product.price, count=count)
    # todo: redirect user to user panel
    # return redirect('/user/orders')
    url_parts = request.path.split('/')
    if url_parts[1] == 'add-link-order-via-registration':
        return redirect('/new_term_book_registration')
    elif url_parts[1] == 'add-link-order-via-productlist':
        return redirect('/products')

    else:
        redirect('/')
