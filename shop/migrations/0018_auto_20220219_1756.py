# Generated by Django 3.2.6 on 2022-02-19 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0013_auto_20220219_1745'),
        ('shop', '0017_auto_20220219_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partplace',
            name='trailer',
        ),
        migrations.AddField(
            model_name='partplace',
            name='trailer',
            field=models.ManyToManyField(to='invent.Trailer'),
        ),
        migrations.RemoveField(
            model_name='partplace',
            name='truck',
        ),
        migrations.AddField(
            model_name='partplace',
            name='truck',
            field=models.ManyToManyField(to='invent.Truck'),
        ),
    ]
