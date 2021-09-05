from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from .managers import DBSearch
from invent.models import Truck, Trailer, Company
from users.models import Profile
from invent.choices import category_choices


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
    mechanic = models.ForeignKey(
        'Mechanic',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    closed = models.DateField(null=True, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return ('Truck ' + self.truck.__str__() if self.truck else
                'Trailer ' + self.trailer.__str__())

    def get_absolute_url(self):
        return reverse('shop:order', kwargs={'pk': self.id})

    def parts_total(self, user):
        parts_total = 0
        parts = self.orderpart_set.all()
        surcharge = user.profile.parts_surcharge
        for p in parts:
            parts_total += p.part.price * surcharge * p.amount
        return parts_total

    @property
    def labor_total(self):
        labor_total = 0
        jobs = self.orderjob_set.all()
        for j in jobs:
            labor_total += j.job.man_hours * j.amount
        return labor_total


class OrderTime(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    start = models.DateTimeField(null=True, blank=True)
    stop = models.DateTimeField(null=True, blank=True)

    @property
    def get_time(self):
        try:
            return self.stop - self.start
        except TypeError:
            return 0


class Part(models.Model):
    part_number = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    stock = models.PositiveSmallIntegerField(default=0)
    stock_unit = models.CharField(max_length=10, blank=True)
    trucks = models.ManyToManyField(Truck, blank=True)
    trailers = models.ManyToManyField(Trailer, blank=True)

    objects = DBSearch()
    # Create index:
    # ALTER TABLE shop_part ADD COLUMN textsearchable_index_col tsvector GENERATED ALWAYS AS (to_tsvector('english', coalesce(part_number, '') || ' ' || coalesce(name, ''))) STORED;
    # CREATE INDEX partsearch_idx ON shop_part USING GIN (textsearchable_index_col);

    class Meta:
        ordering = ['part_number']

    def __str__(self):
        return self.part_number + ' ' + self.name

    def get_absolute_url(self):
        return reverse('shop:part', kwargs={'pk': self.id})

    @property
    def price(self):
        last_purchase = self.purchaseitem_set.last()
        return last_purchase.price


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
    total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

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


class Mechanic(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Balance(models.Model):
    date = models.DateField()
    category = models.CharField(
        max_length=2,
        choices=category_choices(),
    )
    total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    comments = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-date', '-id']


class Inspection(models.Model):
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='truck_pms',
    )
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='trailer_pms',
    )
    date = models.DateField(null=True, blank=True, default=now)
    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    tires = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        null=True,
        blank=True,
    )
    brakes = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return ('Truck ' + self.truck.__str__() + ': DOT #' + str(self.id)
                if self.truck else 'Trailer ' + self.trailer.__str__() +
                ': DOT #' + str(self.id))

    def get_absolute_url(self):
        return reverse('shop:inspection', kwargs={'pk': self.id})
