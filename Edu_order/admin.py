from django.contrib import admin

# Register your models here.
from Edu_order.models import Order, OrderDetail


class OrderRegisterAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_paid', 'payment_date']


admin.site.register(Order, OrderRegisterAdmin)
admin.site.register(OrderDetail)
