from django.urls import path

from Edu_order.views import add_user_order, user_open_order, remove_order_detail, verify, send_request, \
    add_user_order_via_link, remove_order_detail_via_new_term_regitration

urlpatterns = [
    path('add-user-order', add_user_order),
    path('open-order', user_open_order),
    path('remove-order-detail/<detail_id>', remove_order_detail),
    path('remove-order-detail-via-new_term_regitration/<ProductId>', remove_order_detail_via_new_term_regitration),
    path('add-link-order-via-registration/<productId>', add_user_order_via_link),
    path('add-link-order-via-productlist/<productId>', add_user_order_via_link),
    path('add-link-order-via-productlist/<productId>', add_user_order_via_link),
    path('request', send_request, name='request'),

    path('verify/<order_id>', verify, name='verify'),


]
