from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

from users.utils import not_empty
from .utils import db_search
from users.models import Account
from .choices import(truck_make_choices,
                     engine_choices,
                     status_choices,
                     trailer_make_choices,
                     year_choices,
                     us_states_choices)


alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class TruckSearch(models.Manager):
    def search(self, query):
        qs = self.get_queryset()
        if not_empty(query):
            qs = db_search(qs, query, 'B',
                           'fleet_number',
                           'owner',
                           'make',
                           'state',
                           'vin',
                           'license_plate',
                           'prepass',
                           'ipass',
                           'ifta',
                           'ny_permit',
                           'eld',
                           )
        return qs


class Truck(models.Model):
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
    owner = models.ForeignKey(
        'contacts.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_trucks',
        db_column='owner_id',
    )
    make = models.CharField(
        max_length=2,
        choices=truck_make_choices(),
        blank=True,
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=year_choices(),
    )
    state = models.CharField(
        max_length=2,
        choices=us_states_choices(),
        blank=True,
    )
    vin = models.CharField(
        max_length=17,
        null=True,
        blank=True,
        validators=[alphanumeric],
        verbose_name='VIN',
    )
    license_plate = models.CharField(
        max_length=8,
        blank=True,
        validators=[alphanumeric]
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    engine = models.CharField(
        max_length=2,
        choices=engine_choices(),
        blank=True,
    )
    engine_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[alphanumeric])
    value = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )
    registration = models.DateField(
        null=True,
        blank=True,
    )
    insurance = models.DateField(
        null=True,
        blank=True,
    )
    insurer = models.ForeignKey(
        'contacts.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='insured_trucks',
        db_column='insurer_id',
    )
    inspection = models.DateField(
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=2,
        choices=status_choices(),
        default='ID',
    )
    gps = models.BooleanField(null=True, blank=True, verbose_name='GPS')
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
    ky_permit = models.BooleanField(
        null=True,
        blank=True,
        verbose_name='KY',
    )
    nm_permit = models.BooleanField(
        null=True,
        blank=True,
        verbose_name='NM',
    )
    or_permit = models.BooleanField(
        null=True,
        blank=True,
        verbose_name='OR',
    )
    eld = models.CharField(
        max_length=18,
        null=True,
        blank=True,
        verbose_name='ELD',
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Started',
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Terminated',
    )

    objects = TruckSearch()

    def __str__(self):
        return self.fleet_number

    def get_absolute_url(self):
        return reverse('invent:update_truck', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not_empty(self.license_plate):
            self.license_plate = self.license_plate.upper()
        if not_empty(self.vin):
            self.vin = self.vin.upper()
        super(Truck, self).save(*args, **kwargs)


class Trailer(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    fleet_number = models.CharField(max_length=8, null=True)
    company = models.ForeignKey('contacts.Company',
                                on_delete=models.SET_NULL,
                                null=True,
                                )
    license_plate = models.CharField(
        max_length=7,
        blank=True,
    )
    make = models.CharField(
        max_length=2,
        choices=trailer_make_choices(),
        blank=True,
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=year_choices(),
    )
    vin = models.CharField(
        max_length=17,
        blank=True,
    )
    status = models.CharField(
        max_length=2,
        choices=status_choices(),
        default='ID',
        blank=True,
    )

    def __str__(self):
        return self.fleet_number

    def get_absolute_url(self):
        return reverse('invent:update_trailer', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not_empty(self.license_plate):
            self.license_plate = self.license_plate.upper()
        if not_empty(self.vin):
            self.vin = self.vin.upper()
        super(Trailer, self).save(*args, **kwargs)
