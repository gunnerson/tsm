# Generated by Django 3.2.6 on 2021-08-15 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210815_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listcolshow',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]
