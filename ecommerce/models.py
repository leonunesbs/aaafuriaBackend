from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile

from io import BytesIO
from PIL import Image as Img

ITEM_SIZES = (
        ('PPBL', 'PPBL'),
        ('PBL', 'PBL'),
        ('MBL', 'MBL'),
        ('GBL', 'GBL'),
        ('GGBL', 'GGBL'),
        ('XGBL', 'XGBL'),
        ('PP', 'PP'),
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
        ('EXGG', 'EXGG'),
    )

PAYMENT_GATEWAYS = (
        ('TR', 'Transferência'),
        ('ST', 'Stripe'),
    )

ORDER_STATUS = (
        ('AG', 'AGUARDANDO'),
        ('PR', 'PROCESSANDO'),
        ('CC', 'CONCLUIDO'),
        ('XX', 'CANCELADO'),
    )
VENDA_GATEWAY = (
        ('O', 'ONLINE'),
        ('P', 'PRESENCIAL'),
    )
class Item(models.Model):
    title = models.CharField(max_length=15)
    image = models.ImageField(blank=True, null=True, upload_to='produtos')

    price = models.FloatField()
    socio_price = models.FloatField()

    has_stock = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)

    has_variations = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            img = Img.open(BytesIO(self.image.read()))
            img.thumbnail((380,380), Img.ANTIALIAS)
            out = BytesIO()
            img.save(out, format='PNG', quality=99)
            out.seek(0)
            self.image = InMemoryUploadedFile(out, 'ImageField', '%s' %self.image.name, 'image/png', out, None)
            super(Item, self).save(*args, **kwargs)

    @receiver(post_save, sender='ecommerce.Item')
    def create_variations(sender, instance, created, **kwargs):
        if created:
            if instance.has_variations:
                for size in ITEM_SIZES:
                    ItemSize.objects.create(item=instance, size=size[1])

    



class ItemSize(models.Model):
    item = models.ForeignKey(Item, related_name='item', on_delete=models.CASCADE)
    size = models.CharField(max_length=4, choices=ITEM_SIZES)
    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.size

    @receiver(post_save, sender='ecommerce.ItemSize')
    def calculate_stock(sender, instance, created, **kwargs):
        stock = 0
        item_variations = ItemSize.objects.filter(item=instance.item)

        for variation in item_variations:
            stock += variation.stock

        instance.item.stock = stock
        instance.item.save()


                


    


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.ForeignKey(ItemSize, on_delete=models.CASCADE, blank=True, null=True)

    quantity = models.FloatField(default=1)
    final_price = models.FloatField()

    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} x {self.item.title}'

        

   



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)

    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    order_total = models.FloatField(default=0)
    status = models.CharField(max_length=2, choices=ORDER_STATUS)

    gateway = models.CharField(choices=VENDA_GATEWAY, max_length=1)

    def __str__(self):
        return self.user.sócio.nome_completo

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.final_price
        return total


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    gateway = models.CharField(choices=PAYMENT_GATEWAYS, max_length=2)
    amount = models.FloatField(default=0)
    comprovante = models.ImageField(upload_to='comprovantes', blank=True, null=True)
    paid = models.BooleanField(default=False)
