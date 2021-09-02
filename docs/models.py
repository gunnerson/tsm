from django.db import models
from django.utils.timezone import now

from shop.models import Order, Inspection
from invent.models import Truck, Trailer, Driver, Company
from invent.choices import file_category_choices


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


class Document(models.Model):
    file = models.FileField()
    category = models.CharField(
        max_length=2,
        choices=file_category_choices(),
        default="GN",
    )
    description = models.CharField(max_length=50)

    class Meta:
        abstract = True
        ordering = ['-id']

    def __str__(self):
        return str(self.description)


class TruckDocument(Document):
    origin = models.ForeignKey(Truck, on_delete=models.CASCADE)


class TrailerDocument(Document):
    origin = models.ForeignKey(Trailer, on_delete=models.CASCADE)


class DriverDocument(Document):
    origin = models.ForeignKey(Driver, on_delete=models.CASCADE)


class CompanyDocument(Document):
    origin = models.ForeignKey(Company, on_delete=models.CASCADE)
