from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.core.validators import RegexValidator

from users.models import Account
from .managers import DBSearch
from .choices import (
    truck_make_choices,
    engine_choices,
    status_choices,
    driver_status_choices,
    trailer_make_choices,
    year_choices,
    us_states_choices,
    company_group_choices,
)


class Truck(models.Model):
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    fleet_number = models.CharField(
        max_length=8,
        null=True,
        validators=[alphanumeric],
    )
    vin = models.CharField(
        max_length=17,
        null=True,
        blank=True,
        verbose_name='VIN',
        validators=[alphanumeric],
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=year_choices(),
    )
    make = models.CharField(
        max_length=2,
        choices=truck_make_choices(),
        blank=True,
    )
    license_plate = models.CharField(
        max_length=8,
        blank=True,
        validators=[alphanumeric],
    )
    state = models.CharField(
        max_length=2,
        choices=us_states_choices(),
        blank=True,
    )
    status = models.CharField(
        max_length=2,
        choices=status_choices(),
        default='I',
    )
    owner = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_trucks',
        db_column='owner',
        limit_choices_to=Q(group='OU') | Q(group='LO'),
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    insurance = models.DateField(
        null=True,
        blank=True,
    )
    insurer = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='insured_trucks',
        db_column='insurer',
        limit_choices_to={'group': 'IN'},
    )
    value = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )
    engine = models.CharField(
        max_length=2,
        choices=engine_choices(),
        blank=True,
    )
    engine_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[alphanumeric]
    )
    registration = models.DateField(
        null=True,
        blank=True,
        verbose_name='Reg exp',
    )
    inspection = models.DateField(
        null=True,
        blank=True,
        verbose_name='Annual exp',
    )
    last_pm_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Last PM',
    )
    last_pm_mls = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='odometer'
    )
    gps = models.BooleanField(verbose_name='GPS', default=False)
    prepass = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='PrePass',
    )
    ipass = models.CharField(
        max_length=14,
        null=True,
        blank=True,
        verbose_name='I-Pass',
    )
    ifta = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        verbose_name='IFTA',
    )
    ny_permit = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name='NY',
    )
    ky_permit = models.BooleanField(verbose_name='KY', default=False)
    nm_permit = models.BooleanField(verbose_name='NM', default=False)
    or_permit = models.BooleanField(verbose_name='OR', default=False)
    eld = models.CharField(
        max_length=18,
        null=True,
        blank=True,
        verbose_name='ELD',
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Start',
    )
    term_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Term',
    )
    objects = DBSearch()
    # Create index:
    # ALTER TABLE invent_truck
    #     ADD COLUMN textsearchable_index_col tsvector
    #                GENERATED ALWAYS AS (to_tsvector('english', coalesce(fleet_number, '') || ' ' || coalesce(license_plate, '') || ' ' || coalesce(vin, ''))) STORED;
    # CREATE INDEX trucksearch_idx ON invent_truck USING GIN (textsearchable_index_col);

    class Meta:
        ordering = ['fleet_number']
        constraints = [models.UniqueConstraint(
            fields=['account', 'vin'], name='unique_truck')]

    def __str__(self):
        return self.fleet_number

    def get_absolute_url(self):
        return reverse('invent:truck', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.license_plate:
            self.license_plate = self.license_plate.upper()
        if self.vin:
            self.vin = self.vin.upper()
        super().save(*args, **kwargs)


class Trailer(models.Model):
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    fleet_number = models.CharField(
        max_length=8,
        null=True,
        validators=[alphanumeric],
    )
    vin = models.CharField(
        max_length=17,
        null=True,
        blank=True,
        validators=[alphanumeric],
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=year_choices(),
    )
    make = models.CharField(
        max_length=2,
        choices=trailer_make_choices(),
        blank=True,
    )
    status = models.CharField(
        max_length=2,
        choices=status_choices(),
        default='I',
        blank=True,
    )
    license_plate = models.CharField(
        max_length=8,
        blank=True,
        validators=[alphanumeric],
    )
    state = models.CharField(
        max_length=2,
        choices=us_states_choices(),
        blank=True,
    )
    owner = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_trailers',
        db_column='owner',
    )
    value = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )
    insurance = models.DateField(
        null=True,
        blank=True,
    )
    insurer = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='insured_trailers',
        db_column='insurer',
        limit_choices_to={'group': 'IN'},
    )
    registration = models.DateField(
        null=True,
        blank=True,
        verbose_name='Reg exp',
    )
    inspection = models.DateField(
        null=True,
        blank=True,
        verbose_name='Annual exp',
    )
    gps = models.BooleanField(verbose_name='GPS', default=False)
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Start',
    )
    term_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Term',
    )

    objects = DBSearch()
    # Create index:
    # ALTER TABLE invent_trailer
    #     ADD COLUMN textsearchable_index_col tsvector
    #                GENERATED ALWAYS AS (to_tsvector('english', coalesce(fleet_number, '') || ' ' || coalesce(license_plate, '') || ' ' || coalesce(vin, ''))) STORED;
    # CREATE INDEX trailersearch_idx ON invent_trailer USING GIN (textsearchable_index_col);

    class Meta:
        ordering = ['fleet_number']
        constraints = [models.UniqueConstraint(
            fields=['account', 'vin'], name='unique_trailer')]

    def __str__(self):
        return str(self.fleet_number)

    def get_absolute_url(self):
        return reverse('invent:trailer', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.license_plate:
            self.license_plate = self.license_plate.upper()
        if self.vin:
            self.vin = self.vin.upper()
        super().save(*args, **kwargs)


class Company(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=20)
    group = models.CharField(
        max_length=2,
        choices=company_group_choices(),
        default='GN',
    )
    comments = models.TextField(blank=True)

    objects = DBSearch()
    # Create index:
    # ALTER TABLE invent_company
    #     ADD COLUMN textsearchable_index_col tsvector
    #                GENERATED ALWAYS AS (to_tsvector('english', coalesce(name, '') || ' ' || coalesce(comments, ''))) STORED;
    # CREATE INDEX companysearch_idx ON invent_company USING GIN (textsearchable_index_col);

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']
        constraints = [models.UniqueConstraint(
            fields=['account', 'group', 'name'], name='unique_company')]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('contacts:company', args=[str(self.id)])


class Driver(models.Model):
    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    ssn_regex = RegexValidator(
        regex=r"^(?!000|666)[0-8][0-9]{2}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}$")
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=40)
    truck = models.OneToOneField(
        Truck,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    trailer = models.OneToOneField(
        Trailer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=Q(group='OU') | Q(group='LO'),
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name='DOB',
    )
    cdl = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='CDL#'
    )
    state = models.CharField(
        max_length=2,
        choices=us_states_choices(),
        blank=True,
    )
    cdl_exp_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='CDL exp'
    )
    medical_exp_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Medical exp'
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Hire Date',
    )
    term_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Term date',
    )
    phone_number = models.CharField(
        validators=[phone_number_regex],
        max_length=16,
        blank=True,
    )
    email = models.EmailField(
        blank=True,
    )
    home_address = models.TextField(
        null=True,
        blank=True,
    )
    ssn = models.CharField(
        validators=[ssn_regex],
        max_length=11,
        blank=True
    )
    last_mvr = models.DateField(
        null=True,
        blank=True
    )
    pre_empl_drugtest = models.BooleanField(
        verbose_name='DrugTest', default=False)
    pre_empl_clearinghouse = models.BooleanField(
        verbose_name='Pre-empl Clearinghouse', default=False)
    pre_empl_verification = models.BooleanField(
        verbose_name='PEV', default=False)
    last_clearinghouse = models.DateField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=2,
        choices=driver_status_choices(),
        default='A',
    )

    objects = DBSearch()
    # Create index:
    # ALTER TABLE invent_driver
    #     ADD COLUMN textsearchable_index_col tsvector
    #                GENERATED ALWAYS AS (to_tsvector('english', coalesce(name, '') || ' ' || coalesce(cdl, '') || ' ' || coalesce(phone_number, '') || ' ' || coalesce(home_address, '') || ' ' || coalesce(ssn, ''))) STORED;
    # CREATE INDEX driversearch_idx ON invent_driver USING GIN (textsearchable_index_col);

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('invent:driver', args=[str(self.id)])


class PasswordGroup(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=24)
    comments = models.TextField()
    url = models.URLField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['account', 'name'], name='password_group')]

    def __str__(self):
        return str(self.name)


class PasswordAccount(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    group = models.ForeignKey(
        PasswordGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=24)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['account', 'name'], name='password_account')]

    def __str__(self):
        return str(self.name)


class PasswordRecord(models.Model):
    account = models.ForeignKey(
        PasswordAccount,
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=24)
    value = models.CharField(max_length=48)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['account', 'name'], name='password_record')]

    def __str__(self):
        return str(self.name)
