from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from invent.models import Truck, Trailer, Company
from users.models import Profile
from invent.choices import mechanic_choices
from users.utils import gen_field_ver_name


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
        return (self.truck.__str__() + ' #' + str(self.id) if self.truck else
                self.trailer.__str__() + ' #' + str(self.id))

    def get_absolute_url(self):
        return reverse('shop:order', kwargs={'pk': self.id})

    # @property
    # def get_fields(self):
    #     return [(gen_field_ver_name(field.verbose_name),
    #              field.value_from_object(self))
    #             for field in self.__class__._meta.fields]


class Part(models.Model):
    part_number = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    stock = models.PositiveSmallIntegerField(default=0)
    stock_unit = models.CharField(max_length=10, blank=True)
    trucks = models.ManyToManyField(Truck, blank=True)
    trailers = models.ManyToManyField(Trailer, blank=True)

    class Meta:
        ordering = ['part_number']

    def __str__(self):
        return self.part_number

    def get_absolute_url(self):
        return reverse('shop:part', kwargs={'pk': self.id})


class PartAmount(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=1)


class Job(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    parts = models.ManyToManyField(PartAmount, blank=True)


class JobItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
        related_name='job_items',
    )
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


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    amount = models.PositiveSmallIntegerField()
