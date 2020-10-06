# Generated by Django 3.1 on 2020-09-28 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0017_item_is_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('AG', 'AGUARDANDO'), ('PR', 'PROCESSANDO'), ('CC', 'CONCLUÍDO'), ('XX', 'CANCELADO')], max_length=2),
        ),
    ]
