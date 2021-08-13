# Generated by Django 3.2.6 on 2021-08-13 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0014_trailer_unique_trailer'),
        ('contacts', '0005_driver_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='truck',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent.truck'),
        ),
    ]
