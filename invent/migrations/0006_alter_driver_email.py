# Generated by Django 3.2.6 on 2021-09-18 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0005_alter_driver_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
            preserve_default=False,
        ),
    ]
