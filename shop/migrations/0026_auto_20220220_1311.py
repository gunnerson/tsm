# Generated by Django 3.2.6 on 2022-02-20 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_auto_20220220_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partplace',
            options={'ordering': ['part__part_type', 'part', 'truck', 'trailer']},
        ),
        migrations.DeleteModel(
            name='Inspection',
        ),
    ]
