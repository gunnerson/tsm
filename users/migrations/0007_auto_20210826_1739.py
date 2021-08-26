# Generated by Django 3.2.6 on 2021-08-26 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_account_db_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preferencelist',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='account',
        ),
        migrations.AddField(
            model_name='profile',
            name='font_size',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='M', max_length=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='labor_rate',
            field=models.PositiveSmallIntegerField(default=100),
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='PreferenceList',
        ),
    ]
