# Generated by Django 3.2.8 on 2022-03-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_part_replaces'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='track',
        ),
        migrations.RemoveField(
            model_name='part',
            name='track_stock',
        ),
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.PositiveSmallIntegerField(default=1)),
                ('part', models.ManyToManyField(blank=True, to='shop.Part')),
            ],
            options={
                'verbose_name_plural': 'shelves',
            },
        ),
    ]
