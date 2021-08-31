from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from .managers import DBSearch
from invent.models import Truck, Trailer, Company
from invent.choices import mechanic_choices


class Order(models.Model):
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    opened = models.DateField(null=True, blank=True, default=now)
    mechanic = models.CharField(
        max_length=2,
        choices=mechanic_choices(),
        null=True,
        blank=True,
        default='VP',
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    closed = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return ('Truck ' + self.truck.__str__() + ': Order #' + str(self.id)
                if self.truck else 'Trailer ' + self.trailer.__str__() +
                ': Order #' + str(self.id))

    def get_absolute_url(self):
        return reverse('shop:order', kwargs={'pk': self.id})


class Part(models.Model):
    part_number = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    stock = models.PositiveSmallIntegerField(default=0)
    stock_unit = models.CharField(max_length=10, blank=True)
    trucks = models.ManyToManyField(Truck, blank=True)
    trailers = models.ManyToManyField(Trailer, blank=True)

    objects = DBSearch()

    class Meta:
        ordering = ['part_number']

    def __str__(self):
        return self.part_number

    def get_absolute_url(self):
        return reverse('shop:part', kwargs={'pk': self.id})


class Job(models.Model):
    name = models.CharField(max_length=50)
    man_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    parts = models.ManyToManyField(Part, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class OrderJob(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        blank=True,
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_items',
    )
    amount = models.PositiveSmallIntegerField(default=1)


class OrderPart(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        blank=True,
    )
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=1)


class Purchase(models.Model):
    vendor = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'group': 'VE'},
    )
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.vendor.__str__() + ' / ' + str(self.date)

    def get_absolute_url(self):
        return reverse('shop:purchase', kwargs={'pk': self.id})


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        blank=True,
    )
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    amount = models.PositiveSmallIntegerField()
