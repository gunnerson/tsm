# Generated by Django 3.2.6 on 2021-08-30 19:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0011_auto_20210830_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='address_line_1',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='company',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='company',
            name='state',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='company',
            name='zip_code',
            field=models.CharField(blank=True, max_length=5, validators=[django.core.validators.RegexValidator('^\\d{5}$', 'Invalid zip-code')]),
        ),
    ]
