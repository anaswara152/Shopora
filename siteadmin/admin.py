from django.contrib import admin
from .models import*
from user.models import Order, OrderItem

# Register your models here.

admin.site.register(category)
admin.site.register(Order)
admin.site.register(OrderItem)