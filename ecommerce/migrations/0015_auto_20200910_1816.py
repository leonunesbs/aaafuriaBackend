# Generated by Django 3.1 on 2020-09-10 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0014_auto_20200910_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='final_price',
            field=models.FloatField(),
        ),
    ]
