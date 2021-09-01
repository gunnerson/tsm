from django.db import models
from django.utils.timezone import now

from shop.models import Order, Inspection
from invent.models import Truck, Trailer


class Image(models.Model):
    image = models.ImageField()
    date = models.DateField(default=now)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.image.url)


class OrderImage(Image):
    origin = models.ForeignKey(Order, on_delete=models.CASCADE)


class InspectionImage(Image):
    origin = models.ForeignKey(Inspection, on_delete=models.CASCADE)


class TruckImage(Image):
    origin = models.ForeignKey(Truck, on_delete=models.CASCADE)


class TrailerImage(Image):
    origin = models.ForeignKey(Trailer, on_delete=models.CASCADE)
