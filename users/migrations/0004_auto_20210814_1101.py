# Generated by Django 3.2.6 on 2021-08-14 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210814_1056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listcolshow',
            old_name='verbose_name',
            new_name='field_verbose_name',
        ),
        migrations.AddField(
            model_name='listcolshow',
            name='list_verbose_name',
            field=models.CharField(default='', max_length=18),
            preserve_default=False,
        ),
    ]
