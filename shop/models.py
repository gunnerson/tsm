from django.db import models
from django.urls import reverse

from invent.models import Truck, Trailer, Company
from users.models import Profile
from invent.choices import mechanic_choices


class Order(models.Model):
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    trailer = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_opened = models.DateField(null=True, blank=True)
    mechanic = models.CharField(
        max_length=2,
        choices=mechanic_choices(),
        null=True,
        blank=True,
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    date_closed = models.DateField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(f'{self.id:05}')

    def get_absolute_url(self):
        return reverse('shop:order', kwargs={'pk': self.id})


class Operation(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )

