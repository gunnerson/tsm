# Generated by Django 3.2.6 on 2022-02-20 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20220220_1052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partplace',
            options={'ordering': ['part', 'truck', 'trailer']},
        ),
        migrations.AddField(
            model_name='job',
            name='part_types',
            field=models.ManyToManyField(blank=True, to='shop.PartType'),
        ),
    ]
