from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta

from .managers import DBSearch
from .choices import (
    truck_make_choices,
    trailer_make_choices,
    year_choices,
    us_states_choices,
    company_group_choices,
)


class Truck(models.Model):
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    fleet_number = models.CharField(
        max_length=8,
        null=True,
        validators=[alphanumeric],
    )
    owner = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_trucks',
        db_column='owner',
        limit_choices_to=Q(group='OU') | Q(group='LO') | Q(group='CS'),
    )
    vin = models.CharField(
        max_length=17,
        null=True,
        blank=True,
        verbose_name='VIN',
        validators=[alphanumeric],
        unique=True,
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
    last_pm_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Last PM Date',
    )
    last_pm_mls = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Last PM Odometer'
    )
    last_dot_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Annual inspection',
    )
    kt_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    odometer = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    show = models.BooleanField(default=True)

    objects = DBSearch()
    # Create index:
    # ALTER TABLE invent_truck ADD COLUMN textsearchable_index_col tsvector GENERATED ALWAYS AS (to_tsvector('english', coalesce(fleet_number, '') || ' ' || coalesce(license_plate, '') || ' ' || coalesce(vin, ''))) STORED;
    # CREATE INDEX trucksearch_idx ON invent_truck USING GIN (textsearchable_index_col);

    class Meta:
        ordering = ['owner', 'fleet_number']
        constraints = [
            models.UniqueConstraint(
                fields=['fleet_number', 'owner'], name='unique_truck'),
        ]

    def __str__(self):
        return 'Trk#' + self.fleet_number + ' ' + self.owner.__str__().split()[0]

    def get_absolute_url(self):
        return reverse('invent:truck', args=[str(self.id)])

    def get_last_dot(self):
        docs = self.truckdocument_set.filter(category='DI')
        return docs.last()

    def save(self, *args, **kwargs):
        if self.vin:
            self.vin = self.vin.upper()
        super().save(*args, **kwargs)

    def get_mls_to_pm(self):
        if self.last_pm_mls and self.odometer:
            return self.odometer - self.last_pm_mls
        else:
            return None

    @ property
    def pm_due(self):
        if self.get_mls_to_pm():
            if self.get_mls_to_pm() > 25000:
                return 'due'
            elif self.get_mls_to_pm() > 20000:
                return 'soon'
        else:
            return None

    @ property
    def dot_due(self):
        if self.last_dot_date:
            now = timezone.now()
            if (now.date() - self.last_dot_date) > timedelta(days=365):
                return 'due'
            elif (now.date() - self.last_dot_date) > timedelta(days=300):
                return 'soon'
        else:
            return None


class Trailer(models.Model):
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    fleet_number = models.CharField(
        max_length=8,
        null=True,
        validators=[alphanumeric],
    )
    owner = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_trailers',
        db_column='owner',
        limit_choices_to=Q(group='OU') | Q(group='LO') | Q(group='CS'),
    )
    vin = models.CharField(
        max_length=17,
        null=True,
        blank=True,
        validators=[alphanumeric],
        unique=True,
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
    last_dot_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Annual inspection',
    )
    show = models.BooleanField(default=True)

    objects = DBSearch()
    # Create index:
    # ALTER TABLE invent_trailer ADD COLUMN textsearchable_index_col tsvector GENERATED ALWAYS AS (to_tsvector('english', coalesce(fleet_number, '') || ' ' || coalesce(license_plate, '') || ' ' || coalesce(vin, ''))) STORED;
    # CREATE INDEX trailersearch_idx ON invent_trailer USING GIN (textsearchable_index_col);

    class Meta:
        ordering = ['fleet_number']
        constraints = [
            models.UniqueConstraint(
                fields=['fleet_number', 'owner'], name='unique_trailer'),
        ]

    def __str__(self):
        return 'Trl#' + self.fleet_number + ' ' + self.owner.__str__().split()[0]

    def get_absolute_url(self):
        return reverse('invent:trailer', args=[str(self.id)])

    def get_last_dot(self):
        docs = self.trailerdocument_set.filter(category='DI')
        return docs.last()

    def save(self, *args, **kwargs):
        if self.vin:
            self.vin = self.vin.upper()
        super().save(*args, **kwargs)

    @ property
    def dot_due(self):
        if self.last_dot_date:
            now = timezone.now()
            if (now.date() - self.last_dot_date) > timedelta(days=365):
                return 'due'
            elif (now.date() - self.last_dot_date) > timedelta(days=300):
                return 'soon'
        else:
            return None


class Company(models.Model):
    zip_code_regex = RegexValidator(r'^\d{5}$', 'Invalid zip-code')
    name = models.CharField(max_length=40)
    group = models.CharField(
        max_length=2,
        choices=company_group_choices(),
    )
    address_line_1 = models.CharField(max_length=30, blank=True)
    address_line_2 = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=15, blank=True)
    state = models.CharField(
        max_length=2,
        choices=us_states_choices(),
        blank=True,
    )
    zip_code = models.CharField(
        max_length=5,
        blank=True,
        validators=[zip_code_regex],
    )
    phone_number = models.CharField(
        max_length=16,
        blank=True,
    )
    email = models.EmailField(
        blank=True,
    )
    comments = models.TextField(blank=True)
    show = models.BooleanField(default=True)

    objects = DBSearch()
    # Create index:
    # ALTER TABLE invent_company ADD COLUMN textsearchable_index_col tsvector GENERATED ALWAYS AS (to_tsvector('english', coalesce(name, '') || ' ' || coalesce(comments, ''))) STORED;
    # CREATE INDEX companysearch_idx ON invent_company USING GIN (textsearchable_index_col);

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']
        constraints = [models.UniqueConstraint(
            fields=['name', 'state'], name='unique_company')]

    def __str__(self):
        return self.name + ' (' + self.state + ')'

    def get_absolute_url(self):
        return reverse('contacts:company', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.phone_number:
            dg = ''.join(i for i in self.phone_number if i.isdigit())
            self.phone_number = '(' + dg[:3] + ') ' + dg[3:6] + '-' + dg[6:]
        super().save(*args, **kwargs)
