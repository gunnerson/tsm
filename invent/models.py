from django.db import models
from django.urls import reverse


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
    year_made = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Year',
    )
    vin = models.CharField(
        max_length=17,
        blank=True,
        verbose_name='VIN',
    )
    lic_plate = models.CharField(
        max_length=7,
        blank=True,
        verbose_name='License plate',
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    engine = models.CharField(
        max_length=2,
        choices=ENGINE,
        blank=True,
    )
    engine_model = models.CharField(max_length=12, blank=True)
    engine_number = models.CharField(max_length=13, blank=True)
    reg_exp = models.DateField(
        null=True,
        blank=True,
        verbose_name='Registraion expiration date',
    )
    ins_exp = models.DateField(
        null=True,
        blank=True,
        verbose_name='Insurance expiration date',
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
                name='unique_truck',
            )
        ]

    def __str__(self):
        return str(self.company) + ' #' + str(self.fleet_number)

    def get_absolute_url(self):
        return reverse('invent:update_truck', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.lic_plate is not None:
            self.lic_plate = self.lic_plate.upper()
        if self.vin is not None:
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
    lic_plate = models.CharField(
        max_length=7,
        blank=True,
        verbose_name='License plate',
    )
    make = models.CharField(
        max_length=2,
        choices=MAKE,
        blank=True,
    )
    year_made = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Year',
    )
    vin = models.CharField(
        max_length=17,
        blank=True,
        verbose_name='VIN',
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
        if self.lic_plate is not None:
            self.lic_plate = self.lic_plate.upper()
        if self.vin is not None:
            self.vin = self.vin.upper()
        super(Trailer, self).save(*args, **kwargs)
