# Generated by Django 3.1 on 2020-09-07 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_associaçãocategoria_reassociação'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='associação',
            options={'verbose_name_plural': 'Associações'},
        ),
        migrations.RenameField(
            model_name='associação',
            old_name='created',
            new_name='created_date',
        ),
    ]
