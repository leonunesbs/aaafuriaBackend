from django.contrib.auth.models import User, Group


from ecommerce.models import Item, OrderItem, Order
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

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


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['items', 'status', 'ordered_date']