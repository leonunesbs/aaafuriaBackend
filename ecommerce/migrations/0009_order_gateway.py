# Generated by Django 3.1 on 2020-09-02 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_auto_20200901_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='gateway',
            field=models.CharField(blank=True, choices=[('O', 'ONLINE'), ('P', 'PRESENCIAL')], max_length=2, null=True),
        ),
    ]
