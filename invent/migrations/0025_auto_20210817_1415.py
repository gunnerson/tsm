# Generated by Django 3.2.6 on 2021-08-17 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0024_alter_truck_vin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='truck',
            name='gps',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='ky_permit',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='nm_permit',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='or_permit',
        ),
    ]
