# Generated by Django 3.2.6 on 2021-08-16 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0022_auto_20210815_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailer',
            name='status',
            field=models.CharField(blank=True, choices=[('DL', 'Trip'), ('ID', 'Idle'), ('SH', 'Shop'), ('IA', 'Sold')], default='ID', max_length=2),
        ),
        migrations.AlterField(
            model_name='truck',
            name='status',
            field=models.CharField(choices=[('DL', 'Trip'), ('ID', 'Idle'), ('SH', 'Shop'), ('IA', 'Sold')], default='ID', max_length=2),
        ),
    ]
