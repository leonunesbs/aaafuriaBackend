from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Sócio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    turma = models.CharField(max_length=2, default='00')
    matrícula = models.CharField(default='00000000', max_length=8)
    is_sócio = models.BooleanField(default=False)
    data_de_nascimento = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.nome_completo

    @receiver(post_save, sender=User)
    def create_user_socio(sender, instance, created, **kwargs):
        if created:
            Sócio.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_socio(sender, instance, **kwargs):
        instance.sócio.save()