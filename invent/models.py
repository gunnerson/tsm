from django.db import models
from django.db.models import Q, UniqueConstraint
from django.urls import reverse
from django.core.validators import RegexValidator

from .utils import db_search
from users.models import Account
from .choices import (
    truck_make_choices,
    engine_choices,
    status_choices,
    trailer_make_choices,
    year_choices,
    us_states_choices,
)


alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class TruckSearch(models.Manager):
    def search(self, query, account):
        qs = self.get_queryset()
        qs = qs.filter(account=account)
        if query:
            qs = db_search(qs, query, 'B',
                           'fleet_number', 'vin', 'license_plate')
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
        default='ID',
    )
    owner = models.ForeignKey(
        'contacts.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_trucks',
        db_column='owner_id',
        limit_choices_to=Q(group='OU') | Q(group='LO'),
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    insurance = models.DateField(
        null=True,
        blank=True,
    )
    insurer = models.ForeignKey(
        'contacts.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='insured_trailers',
        db_column='insurer_id',
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
    )
    inspection = models.DateField(
        null=True,
        blank=True,
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
        verbose_name='Started',
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Terminated',
    )

    objects = TruckSearch()
    # Create index:
    # ALTER TABLE invent_truck
    #     ADD COLUMN textsearchable_index_col tsvector
    #                GENERATED ALWAYS AS (to_tsvector('english', coalesce(fleet_number, '') || ' ' || coalesce(license_plate, '') || ' ' || coalesce(vin, ''))) STORED;
    # CREATE INDEX trucksearch_idx ON invent_truck USING GIN (textsearchable_index_col);

    class Meta:
        ordering = ['fleet_number']

    UniqueConstraint(fields=['account', 'vin'], name='unique_truck')

    def __str__(self):
        return self.fleet_number

    def get_absolute_url(self):
        return reverse('invent:update_truck', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.license_plate:
            self.license_plate = self.license_plate.upper()
        if self.vin:
            self.vin = self.vin.upper()
        super(Truck, self).save(*args, **kwargs)


class Trailer(models.Model):
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
        default='ID',
        blank=True,
    )
    license_plate = models.CharField(
        max_length=8,
        blank=True,
        validators=[alphanumeric],
    )
    company = models.ForeignKey('contacts.Company',
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
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
        'contacts.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='insured_trucks',
        db_column='insurer_id',
        limit_choices_to={'group': 'IN'},
    )
    registration = models.DateField(
        null=True,
        blank=True,
    )
    inspection = models.DateField(
        null=True,
        blank=True,
    )
    gps = models.BooleanField(verbose_name='GPS', default=False)
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

    class Meta:
        ordering = ['fleet_number']

    def __str__(self):
        return str(self.fleet_number)

    def get_absolute_url(self):
        return reverse('invent:update_trailer', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.license_plate:
            self.license_plate = self.license_plate.upper()
        if self.vin:
            self.vin = self.vin.upper()
        super(Trailer, self).save(*args, **kwargs)

    UniqueConstraint(fields=['account', 'vin'], name='unique_trailer')
