from django.db import models
from django.urls import reverse


class Truck(models.Model):
    VOLVO = 'VL'
    FREIGHTLINER = 'FL'
    KENWORTH = 'KW'
    PETERBILT = 'PB'
    MAKE = [
        (VOLVO, 'Volvo'),
        (FREIGHTLINER, 'Freighliner'),
        (KENWORTH, 'Kenworth'),
        (PETERBILT, 'Peterbilt'),
    ]
    fleet_number = models.CharField(max_length=8)
    lic_plate = models.CharField(max_length=8, null=True, blank=True)
    make = models.CharField(
        max_length=2,
        choices=MAKE,
        null=True,
        blank=True,
    )
    model = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return str(self.fleet_number)

    def get_absolute_url(self):
        return reverse('invent:truck_detail', args=[str(self.id)])
