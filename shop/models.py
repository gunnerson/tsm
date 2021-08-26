from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from invent.models import Truck, Trailer, Company
from users.models import Profile, Account
from invent.choices import mechanic_choices


class Order(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
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
    date_opened = models.DateField(null=True, blank=True)
    mechanic = models.CharField(
        max_length=2,
        choices=mechanic_choices(),
        null=True,
        blank=True,
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    date_closed = models.DateField(null=True, blank=True)
    stdopitems = models.ManyToManyField('StdOpItem')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(f'{self.id:05}')

    def get_absolute_url(self):
        return reverse('shop:order', kwargs={'pk': self.id})

    def is_closed(self):
        return True if self.date_closed else False


class Part(models.Model):
    part_number = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    stock = models.PositiveSmallIntegerField(default=0)
    stock_unit = models.CharField(max_length=10, default=True)
    trucks = models.ManyToManyField(Truck)
    trailers = models.ManyToManyField(Trailer)

    class Meta:
        ordering = ['part_number']

    def __str__(self):
        return self.part_number

    def get_absolute_url(self):
        return reverse('shop:part', kwargs={'pk': self.id})


class PartOrder(models.Model):
    vendor = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        limit_choices_to={'group': 'VE'},
    )
    date = models.DateField()

    class Meta:
        ordering = ['-date']


class PartOrderItem(models.Model):
    partorder = models.ForeignKey(PartOrder, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    amount = models.PositiveSmallIntegerField()


class PartsAmount(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()


class StdOp(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    parts = models.ManyToManyField(PartsAmount)
    pm = models.BooleanField(default=False)


class StdOpItem(models.Model):
    stdop = models.ForeignKey(
        StdOp,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    started = models.DateTimeField(default=now)
    finished = models.DateTimeField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.stdop:
    #         new_stdop = StdOp(
    #             name=self.name,
    #             duration=self.duration,
    #             ).save()
    #         new_stdop.parts.add(self.parts)
    #         self.stdop = new_stdop
    #         self.name = ""
    #         self.duration = None
    #         self.parts.clear()
    #     super().save(*args, **kwargs)
