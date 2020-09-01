from django.contrib.auth.models import User, Group


from ecommerce.models import Item, OrderItem, Order, Payment
from core.models import Sócio
from rest_framework import serializers



class SócioSerializer(serializers.ModelSerializer):
    nome_completo = serializers.StringRelatedField()
    class Meta:
        model = Sócio
        fields = ['nome_completo']

class UserSerializer(serializers.ModelSerializer):
    sócio = SócioSerializer()
    class Meta:
        model = User
        fields = ['username', 'email', 'sócio']
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['pk', 'title', 'price', 'socio_price', 'has_variations', 'image']

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
    payment = PaymentSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['pk', 'user', 'items', 'status', 'ordered_date', 'order_total', 'payment']