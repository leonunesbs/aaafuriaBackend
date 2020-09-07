from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

FLUXO_FINANCEIRO = (
    ('E', 'ENTRADA'),
    ('S', 'SAÍDA'),
    ('R', 'REALOCAÇÃO'),
)
ASSOCIAÇÃO_TIPO = (
    ('S', 'SEMESTRAL'),
    ('A', 'ANUAL'),
)


class Sócio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField()
    turma = models.CharField(max_length=2)
    matrícula = models.CharField(max_length=8)
    is_sócio = models.BooleanField(default=False)
    data_de_nascimento = models.DateField(blank=True, null=True)
    celular = models.CharField(max_length=16)
    cpf = models.CharField(max_length=14)
    foto = models.ImageField(upload_to='socios', blank=True, null=True)

    def __str__(self):
        return self.nome_completo

    @receiver(post_save, sender=User)
    def create_user_socio(sender, instance, created, **kwargs):
        if created:
            Sócio.objects.create(user=instance)


class AssociaçãoCategoria(models.Model):
    duração = models.CharField(choices=ASSOCIAÇÃO_TIPO, max_length=1)
    valor = models.FloatField()
    reassociação = models.FloatField()

    def __str__(self):
        return self.get_duração_display()

    class Meta:
        verbose_name = 'Associação Categoria'
        verbose_name_plural = 'Associação Categorias'


class Associação(models.Model):
    sócio = models.OneToOneField(Sócio, on_delete=models.CASCADE)
    categoria = models.ForeignKey(
        AssociaçãoCategoria, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Associações'


class Financeiro(models.Model):
    fluxo = models.CharField(max_length=1, choices=FLUXO_FINANCEIRO)
    finalidade = models.CharField(max_length=50)
    valor = models.FloatField()
    observações = models.TextField(blank=True, null=True)
    responsável = models.CharField(max_length=25)
    data_da_movimentação = models.DateField()
