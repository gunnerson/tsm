# Generated by Django 3.2.8 on 2021-11-30 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20211130_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertime',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.order'),
        ),
    ]
