# Generated by Django 3.2.8 on 2022-04-22 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_auto_20220411_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='category',
            field=models.CharField(choices=[('I', '+Invoice'), ('R', '+Refund'), ('B', '-Building'), ('S', '-Salaries'), ('T', '-Tools'), ('P', '-Parts'), ('E', '-Shop Supplies')], max_length=2),
        ),
    ]
