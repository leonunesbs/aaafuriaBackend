from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import OrderItem
from core.models import Associação

# Final price calculator


@receiver(pre_save, sender=OrderItem)
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
        final_price = price * quantity
        instance.final_price = final_price
