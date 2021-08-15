from django.db import models
from django.urls import reverse

from .utils import not_empty


class Truck(models.Model):
    VOLVO = 'VL'
    FREIGHTLINER = 'FL'
    KENWORTH = 'KW'
    PETERBILT = 'PB'
    INTERNATIONAL = 'IN'
    WESTERN = 'WS'
    CUMMINS = 'CM'
    PACCAR = 'PC'
    DETROIT = 'DT'
    CATERPILLAR = 'CT'
    DELIVERY = 'DL'
    IDLE = 'ID'
    SHOP = 'SH'
    INACTIVE = 'IA'
    MAKE = [
        (FREIGHTLINER, 'Freighliner'),
        (INTERNATIONAL, 'International'),
        (KENWORTH, 'Kenworth'),
        (PETERBILT, 'Peterbilt'),
        (VOLVO, 'Volvo'),
        (WESTERN, 'Western Star'),
    ]
    ENGINE = [
        (CATERPILLAR, 'Caterpillar'),
        (CUMMINS, 'Cummins'),
        (DETROIT, 'Detroit'),
        (INTERNATIONAL, 'International'),
        (PACCAR, 'Paccar'),
        (VOLVO, 'Volvo'),
    ]
    STATUS = [
        (DELIVERY, 'On delivery'),
        (IDLE, 'Idle'),
        (SHOP, 'In the shop'),
        (INACTIVE, 'Inactive'),
    ]
    fleet_number = models.CharField(max_length=8, null=True,)
    company = models.ForeignKey('contacts.Company',
                                on_delete=models.SET_NULL,
                                null=True,
                                )
    make = models.CharField(
        max_length=2,
        choices=MAKE,
        blank=True,
    )
    model = models.CharField(max_length=12, blank=True)
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    vin = models.CharField(
        max_length=17,
        blank=True,
    )
    license_plate = models.CharField(
        max_length=7,
        blank=True,
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    engine = models.CharField(
        max_length=2,
        choices=ENGINE,
        blank=True,
    )
    engine_number = models.CharField(max_length=13, blank=True)
    registration = models.DateField(
        null=True,
        blank=True,
    )
    insurance = models.DateField(
        null=True,
        blank=True,
    )
    inspection = models.DateField(
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default='ID',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fleet_number', 'company'],
                name='unique_truck',
            )
        ]

    def __str__(self):
        return str(self.company) + ' #' + str(self.fleet_number)

    def get_absolute_url(self):
        return reverse('invent:update_truck', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not_empty(self.license_plate):
            self.license_plate = self.license_plate.upper()
        if not_empty(self.vin):
            self.vin = self.vin.upper()
        super(Truck, self).save(*args, **kwargs)


class Trailer(models.Model):
    HYUNDAI = 'HY'
    UTILITY = 'UT'
    WABASH = 'WB'
    DELIVERY = 'DL'
    IDLE = 'ID'
    SHOP = 'SH'
    INACTIVE = 'IA'
    MAKE = [
        (HYUNDAI, 'Hyundai'),
        (UTILITY, 'Utility'),
        (WABASH, 'Wabash'),
    ]
    STATUS = [
        (DELIVERY, 'On delivery'),
        (IDLE, 'Idle'),
        (SHOP, 'In the shop'),
        (INACTIVE, 'Inactive'),
    ]
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
        choices=MAKE,
        blank=True,
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    vin = models.CharField(
        max_length=17,
        blank=True,
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default='ID',
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fleet_number', 'company'],
                name='unique_trailer',
            )
        ]

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
