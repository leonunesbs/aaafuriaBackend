from rest_framework import serializers

from .models import Item, OrderItem, Order, Payment
from core.serializers import UserSerializer



class OrderItemSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    size = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = ['pk', 'item', 'quantity', 'final_price', 'size']

class PaymentSerializer(serializers.ModelSerializer):
    gateway = serializers.StringRelatedField(source='get_gateway_display')
    class Meta:
        model = Payment
        fields = ['gateway']
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.StringRelatedField(source='get_status_display')
    payment = PaymentSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['pk', 'user', 'items', 'status', 'ordered_date', 'order_total', 'payment']


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['pk', 'title', 'price', 'socio_price', 'has_variations', 'image']