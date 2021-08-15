# Generated by Django 3.2.6 on 2021-08-15 23:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0021_auto_20210815_1233'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='truck',
            name='unique_truck',
        ),
        migrations.AddField(
            model_name='truck',
            name='eld',
            field=models.CharField(blank=True, max_length=18, null=True, verbose_name='ELD'),
        ),
        migrations.AddField(
            model_name='truck',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Terminated'),
        ),
        migrations.AddField(
            model_name='truck',
            name='gps',
            field=models.BooleanField(blank=True, null=True, verbose_name='GPS'),
        ),
        migrations.AddField(
            model_name='truck',
            name='ifta',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='IFTA'),
        ),
        migrations.AddField(
            model_name='truck',
            name='ipass',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='I-Pass'),
        ),
        migrations.AddField(
            model_name='truck',
            name='ky_permit',
            field=models.BooleanField(blank=True, null=True, verbose_name='KY'),
        ),
        migrations.AddField(
            model_name='truck',
            name='nm_permit',
            field=models.BooleanField(blank=True, null=True, verbose_name='NM'),
        ),
        migrations.AddField(
            model_name='truck',
            name='ny_permit',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='NY'),
        ),
        migrations.AddField(
            model_name='truck',
            name='or_permit',
            field=models.BooleanField(blank=True, null=True, verbose_name='OR'),
        ),
        migrations.AddField(
            model_name='truck',
            name='prepass',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='PrePass'),
        ),
        migrations.AddField(
            model_name='truck',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Started'),
        ),
        migrations.AlterField(
            model_name='truck',
            name='vin',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')], verbose_name='VIN'),
        ),
    ]
