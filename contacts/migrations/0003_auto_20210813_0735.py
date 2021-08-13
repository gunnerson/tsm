# Generated by Django 3.2.6 on 2021-08-13 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0008_auto_20210812_2120'),
        ('contacts', '0002_alter_company_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='trailer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent.trailer'),
        ),
        migrations.AddField(
            model_name='driver',
            name='truck',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent.truck'),
        ),
    ]
