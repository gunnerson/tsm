# Generated by Django 3.2.6 on 2021-09-18 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210905_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punchcard',
            name='lunch_in_distance',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='punchcard',
            name='lunch_out_distance',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='punchcard',
            name='punch_in_distance',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='punchcard',
            name='punch_out_distance',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
    ]
