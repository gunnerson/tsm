# Generated by Django 3.2.8 on 2022-03-11 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_auto_20220301_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechanic',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True),
        ),
    ]
