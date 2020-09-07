from .models import Associação
from django.dispatch import receiver
assofrom django.db.models.signals import post_save


@receiver(post_save, sender=Associação)
def set_is_sócio(sender, instance, **kwargs):
    if not instance.sócio.is_sócio:
        instance.sócio.is_sócio = instance.is_active
        instance.sócio.save()
