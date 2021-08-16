# Generated by Django 3.2.6 on 2021-08-16 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_listcolshow_show'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreferanceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trucks_font', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='M', max_length=1, verbose_name='Trucks List Font Size')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
