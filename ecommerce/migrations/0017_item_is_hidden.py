# Generated by Django 3.1 on 2020-09-11 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0016_auto_20200910_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]