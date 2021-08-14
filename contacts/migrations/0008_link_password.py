# Generated by Django 3.2.6 on 2021-08-14 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_alter_driver_truck'),
    ]

    operations = [
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, null=True)),
                ('login', models.CharField(max_length=24, null=True)),
                ('password', models.CharField(max_length=24, null=True)),
                ('group', models.CharField(choices=[('PP', 'PrePass'), ('NP', 'NY Permit'), ('OT', 'Other')], max_length=2, null=True)),
                ('comments', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.URLField(null=True)),
                ('password', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.password')),
            ],
        ),
    ]