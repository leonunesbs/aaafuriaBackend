# Generated by Django 3.1 on 2020-09-02 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200902_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financeiro',
            name='data_da_movimentação',
            field=models.DateField(),
        ),
    ]
