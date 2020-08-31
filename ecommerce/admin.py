from django.contrib import admin
from .models import Item, ItemSize, OrderItem, Order, Payment


admin.site.register(Item)
admin.site.register(ItemSize)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)

