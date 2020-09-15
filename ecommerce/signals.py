from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import OrderItem, Order
from core.models import Associação

# Final price calculator


@receiver(pre_save, sender=OrderItem)
# Calcula o preço final de um item verificando se o dono do item é sócio
def final_price_calculator(sender, instance, **kwargs):
    price = instance.item.price
    socio_price = instance.item.socio_price
    quantity = instance.quantity
    associação = Associação.objects.filter(sócio=instance.user.sócio)
    if associação.exists():
        if associação.first().is_active:
            final_price = socio_price * quantity
            instance.final_price = final_price
    else:
        instance.final_price = price * quantity


@receiver(post_save, sender=Order)
# Marca pedidos como não Ordered ao serem cancelados
def final_price_calculator(sender, instance, **kwargs):
    if instance.status == 'XX':
        instance.items.all().update(ordered=False)
