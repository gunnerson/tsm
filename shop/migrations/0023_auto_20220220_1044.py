# Generated by Django 3.2.6 on 2022-02-20 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_auto_20220219_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partplace',
            name='axle_add',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='partplace',
            name='axle_drv',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='partplace',
            name='axle_str',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='partplace',
            name='axle_trl',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='partplace',
            name='side_left',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='partplace',
            name='side_right',
            field=models.BooleanField(default=False),
        ),
    ]
