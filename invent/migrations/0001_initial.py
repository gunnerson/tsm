# Generated by Django 3.2.6 on 2021-09-01 12:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('group', models.CharField(choices=[('OU', 'Ours'), ('LO', 'Logistics'), ('IN', 'Insurance'), ('VE', 'Vendors'), ('CS', 'Customers')], default='GN', max_length=2)),
                ('address_line_1', models.CharField(blank=True, max_length=30)),
                ('address_line_2', models.CharField(blank=True, max_length=10)),
                ('city', models.CharField(blank=True, max_length=15)),
                ('state', models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('zip_code', models.CharField(blank=True, max_length=5, validators=[django.core.validators.RegexValidator('^\\d{5}$', 'Invalid zip-code')])),
                ('phone_number', models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('comments', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PasswordGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True)),
                ('comments', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True)),
                ('value', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fleet_number', models.CharField(max_length=8, null=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('vin', models.CharField(blank=True, max_length=17, null=True, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')], verbose_name='VIN')),
                ('year', models.PositiveSmallIntegerField(blank=True, choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], null=True)),
                ('make', models.CharField(blank=True, choices=[('FL', 'Freighliner'), ('IN', 'International'), ('KW', 'Kenworth'), ('PB', 'Peterbilt'), ('VL', 'Volvo'), ('WS', 'Western Star')], max_length=2)),
                ('license_plate', models.CharField(blank=True, max_length=8, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('state', models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('status', models.CharField(choices=[('D', 'Delivery'), ('I', 'Idle'), ('S', 'Shop'), ('T', 'Term')], default='I', max_length=2)),
                ('mileage', models.PositiveIntegerField(blank=True, null=True)),
                ('insurance', models.DateField(blank=True, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('engine', models.CharField(blank=True, choices=[('CT', 'Caterpillar'), ('CM', 'Cummins'), ('DT', 'Detroit'), ('IN', 'International'), ('PC', 'Paccar'), ('VL', 'Volvo')], max_length=2)),
                ('engine_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('registration', models.DateField(blank=True, null=True, verbose_name='Reg exp')),
                ('inspection', models.DateField(blank=True, null=True, verbose_name='Annual exp')),
                ('last_pm_date', models.DateField(blank=True, null=True, verbose_name='Last PM')),
                ('last_pm_mls', models.PositiveIntegerField(blank=True, null=True, verbose_name='odometer')),
                ('gps', models.BooleanField(default=False, verbose_name='GPS')),
                ('prepass', models.PositiveIntegerField(blank=True, null=True, verbose_name='PrePass')),
                ('ipass', models.CharField(blank=True, max_length=14, null=True, verbose_name='I-Pass')),
                ('ifta', models.CharField(blank=True, max_length=12, null=True, verbose_name='IFTA')),
                ('ny_permit', models.CharField(blank=True, max_length=6, null=True, verbose_name='NY')),
                ('ky_permit', models.BooleanField(default=False, verbose_name='KY')),
                ('nm_permit', models.BooleanField(default=False, verbose_name='NM')),
                ('or_permit', models.BooleanField(default=False, verbose_name='OR')),
                ('eld', models.CharField(blank=True, max_length=18, null=True, verbose_name='ELD')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start')),
                ('term_date', models.DateField(blank=True, null=True, verbose_name='Term')),
                ('insurer', models.ForeignKey(blank=True, db_column='insurer', limit_choices_to={'group': 'IN'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='insured_trucks', to='invent.company')),
                ('owner', models.ForeignKey(blank=True, db_column='owner', limit_choices_to=models.Q(('group', 'OU'), ('group', 'LO'), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_trucks', to='invent.company')),
            ],
            options={
                'ordering': ['fleet_number'],
            },
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fleet_number', models.CharField(max_length=8, null=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('vin', models.CharField(blank=True, max_length=17, null=True, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('year', models.PositiveSmallIntegerField(blank=True, choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], null=True)),
                ('make', models.CharField(blank=True, choices=[('HY', 'Hyundai'), ('UT', 'Utility'), ('WB', 'Wabash')], max_length=2)),
                ('status', models.CharField(blank=True, choices=[('D', 'Delivery'), ('I', 'Idle'), ('S', 'Shop'), ('T', 'Term')], default='I', max_length=2)),
                ('license_plate', models.CharField(blank=True, max_length=8, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('state', models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('insurance', models.DateField(blank=True, null=True)),
                ('registration', models.DateField(blank=True, null=True, verbose_name='Reg exp')),
                ('inspection', models.DateField(blank=True, null=True, verbose_name='Annual exp')),
                ('gps', models.BooleanField(default=False, verbose_name='GPS')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start')),
                ('term_date', models.DateField(blank=True, null=True, verbose_name='Term')),
                ('insurer', models.ForeignKey(blank=True, db_column='insurer', limit_choices_to={'group': 'IN'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='insured_trailers', to='invent.company')),
                ('owner', models.ForeignKey(blank=True, db_column='owner', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_trailers', to='invent.company')),
            ],
            options={
                'ordering': ['fleet_number'],
            },
        ),
        migrations.CreateModel(
            name='PasswordAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent.passwordgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='DOB')),
                ('cdl', models.CharField(blank=True, max_length=20, verbose_name='CDL#')),
                ('cdl_exp_date', models.DateField(blank=True, null=True, verbose_name='CDL exp')),
                ('medical_exp_date', models.DateField(blank=True, null=True, verbose_name='Medical exp')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Hire Date')),
                ('term_date', models.DateField(blank=True, null=True, verbose_name='Term date')),
                ('phone_number', models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address_line_1', models.CharField(blank=True, max_length=30)),
                ('address_line_2', models.CharField(blank=True, max_length=10)),
                ('city', models.CharField(blank=True, max_length=15)),
                ('state', models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('zip_code', models.CharField(blank=True, max_length=5, validators=[django.core.validators.RegexValidator('^\\d{5}$', 'Invalid zip-code')])),
                ('ssn', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator(regex='^(?!000|666)[0-8][0-9]{2}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}$')])),
                ('last_mvr', models.DateField(blank=True, null=True)),
                ('pre_empl_drugtest', models.BooleanField(default=False, verbose_name='DrugTest')),
                ('pre_empl_clearinghouse', models.BooleanField(default=False, verbose_name='Pre-empl Clearinghouse')),
                ('pre_empl_verification', models.BooleanField(default=False, verbose_name='PEV')),
                ('last_clearinghouse', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('T', 'Term')], default='A', max_length=2)),
                ('owner', models.ForeignKey(blank=True, limit_choices_to=models.Q(('group', 'OU'), ('group', 'LO'), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, to='invent.company', verbose_name='Company')),
                ('trailer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invent.trailer')),
                ('truck', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invent.truck')),
            ],
        ),
        migrations.AddConstraint(
            model_name='company',
            constraint=models.UniqueConstraint(fields=('group', 'name'), name='unique_company'),
        ),
    ]
