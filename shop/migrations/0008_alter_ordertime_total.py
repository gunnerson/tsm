# Generated by Django 3.2.6 on 2021-09-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210905_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertime',
            name='total',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
        ),
    ]
