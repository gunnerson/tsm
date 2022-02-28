# Generated by Django 3.2.6 on 2022-02-20 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20220220_1044'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='partplace',
            constraint=models.UniqueConstraint(fields=('part', 'truck'), name='unique_truck_part'),
        ),
        migrations.AddConstraint(
            model_name='partplace',
            constraint=models.UniqueConstraint(fields=('part', 'trailer'), name='unique_trailer_part'),
        ),
    ]