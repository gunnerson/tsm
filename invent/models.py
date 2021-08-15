from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

from users.utils import not_empty
from users.models import Account
from .choices import(truck_make_choices,
                     engine_choices,
                     status_choices,
                     trailer_make_choices,
                     year_choices,
                     us_states_choices)


alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


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
        validators=[alphanumeric]
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['account', 'vin'],
                name='unique_truck',
            )
        ]

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

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['fleet_number', 'company'],
    #             name='unique_trailer',
    #         )
    #     ]

    def __str__(self):
        return str(self.company) + ' #' + str(self.fleet_number)

    def get_absolute_url(self):
        return reverse('invent:update_trailer', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not_empty(self.license_plate):
            self.license_plate = self.license_plate.upper()
        if not_empty(self.vin):
            self.vin = self.vin.upper()
        super(Trailer, self).save(*args, **kwargs)
