# Generated by Django 3.2.6 on 2021-10-28 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0005_auto_20210906_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydocument',
            name='description',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='driverdocument',
            name='description',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='trailerdocument',
            name='description',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='truckdocument',
            name='description',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
