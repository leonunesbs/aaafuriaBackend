# Generated by Django 3.1 on 2020-09-03 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200902_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financeiro',
            name='observações',
            field=models.TextField(blank=True, null=True),
        ),
    ]