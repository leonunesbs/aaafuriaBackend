# Generated by Django 3.1 on 2020-09-06 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_auto_20200901_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
    ]