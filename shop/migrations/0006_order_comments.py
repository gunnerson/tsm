# Generated by Django 3.2.6 on 2021-09-01 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
