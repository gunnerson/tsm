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
    fleet_number = models.CharField(max_length=5, null=True)
    company =  models.ForeignKey('contacts.Company',
                           on_delete=models.SET_NULL,
                           null=True,
                           )
    make = models.CharField(
        max_length=2,
        choices=MAKE,
        null=True,
        blank=True,
    )
    model = models.CharField(max_length=12, null=True, blank=True)
    year_made = models.IntegerField(
        null=True,
        blank=True,
    )
    vin = models.CharField(max_length=17, null=True, blank=True)
    lic_plate = models.CharField(max_length=7, null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    engine = models.CharField(
        max_length=2,
        choices=ENGINE,
        null=True,
        blank=True,
    )
    engine_model = models.CharField(max_length=12, null=True, blank=True)
    engine_number = models.CharField(max_length=13, null=True, blank=True)
    reg_exp = models.DateField(null=True, blank=True)
    ins_exp = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.fleet_number)

    def get_absolute_url(self):
        return reverse('invent:update_truck', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.fleet_number = self.fleet_number.upper()
        if self.lic_plate is not None:
            self.lic_plate = self.lic_plate.upper()
        if self.vin is not None:
            self.vin = self.vin.upper()
        super(Truck, self).save(*args, **kwargs)


class Trailer(models.Model):
    HYUNDAI = 'HY'
    UTILITY = 'UT'
    WABASH = 'WB'
    MAKE = [
        (HYUNDAI, 'Hyundai'),
        (UTILITY, 'Utility'),
        (WABASH, 'Wabash'),
    ]
    fleet_number = models.CharField(max_length=5, null=True)
    company =  models.ForeignKey('contacts.Company',
                               on_delete=models.SET_NULL,
                               null=True,
                               )
    lic_plate = models.CharField(max_length=7, null=True, blank=True)
    make = models.CharField(
        max_length=2,
        choices=MAKE,
        null=True,
        blank=True,
    )
    year_made = models.IntegerField(null=True, blank=True)
    vin = models.CharField(max_length=17, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.fleet_number)

    def get_absolute_url(self):
        return reverse('invent:update_trailer', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.fleet_number = self.fleet_number.upper()
        if self.lic_plate is not None:
            self.lic_plate = self.lic_plate.upper()
        if self.vin is not None:
            self.vin = self.vin.upper()
        super(Trailer, self).save(*args, **kwargs)
