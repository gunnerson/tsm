# Generated by Django 3.2.6 on 2021-09-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0006_alter_driver_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phone_number',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
