# Generated by Django 3.0.4 on 2020-07-06 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='address',
            table='qb_address',
        ),
        migrations.AlterModelTable(
            name='user',
            table='qb_user',
        ),
    ]
