# Generated by Django 3.2.8 on 2022-04-06 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0013_auto_20220219_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='trailer',
            name='last_dot_date',
            field=models.DateField(blank=True, null=True, verbose_name='Annual inspection'),
        ),
        migrations.AddField(
            model_name='truck',
            name='last_dot_date',
            field=models.DateField(blank=True, null=True, verbose_name='Annual inspection'),
        ),
    ]
