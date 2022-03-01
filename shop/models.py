from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from decimal import Decimal

from .managers import DBSearch
from invent.models import Truck, Trailer, Company
from users.models import Profile
from invent.choices import category_choices, parttype_axle_choices, parttype_side_choices


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
        return self.truck.__str__() if self.truck else self.trailer.__str__()

    def get_absolute_url(self):
        return reverse('shop:order', kwargs={'pk': self.id})

    def parts_total(self, user):
        parts_total = 0
        parts = self.orderpart_set.all()
        # surcharge = user.profile.parts_surcharge
        for p in parts:
            try:
                # parts_total += p.part.price * surcharge * p.amount
                parts_total += p.part.price * p.amount
            except TypeError:
                pass
        return round(parts_total, 2)

    @property
    def labor_total(self):
        labor_total = 0
        jobs = self.orderjob_set.all()
        for j in jobs:
            labor_total += j.job.man_hours * j.amount
        return labor_total

    @property
    def taken(self):
        return True if self.ordertime.start else False


class OrderTime(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    start = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0,
    )
    mechanic = models.ForeignKey(
        'Mechanic',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.order.__str__()

    def get_total(self):
        td = now() - self.start
        self.total += Decimal(round((td.seconds / 3600), 1))
        self.start = None
        self.save(update_fields=['total', 'start'])


class PartType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Part(models.Model):
    part_number = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    stock = models.PositiveSmallIntegerField(default=0)
    stock_unit = models.CharField(max_length=10, blank=True)
    trucks = models.ManyToManyField(Truck, blank=True)
    trailers = models.ManyToManyField(Trailer, blank=True)
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
    )
    part_type = models.ForeignKey(
        PartType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    replaces = models.ManyToManyField('Part', blank=True)
    objects = DBSearch()
    # Create index:
    # ALTER TABLE shop_part ADD COLUMN textsearchable_index_col tsvector GENERATED ALWAYS AS (to_tsvector('english', coalesce(part_number, '') || ' ' || coalesce(name, ''))) STORED;
    # CREATE INDEX partsearch_idx ON shop_part USING GIN (textsearchable_index_col);

    class Meta:
        ordering = ['part_number']
        constraints = [
            models.UniqueConstraint(
                fields=['part_number', 'name'], name='unique_part'),
        ]

    def __str__(self):
        return self.part_number + ' ' + self.name

    def get_absolute_url(self):
        return reverse('shop:part', kwargs={'pk': self.id})

    @property
    def get_price(self):
        last_purchase = self.purchaseitem_set.last()
        try:
            return last_purchase.price
        except AttributeError:
            return 0


class PartPlace(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    truck = models.ForeignKey(
        Truck,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    side_left = models.BooleanField(default=False)
    side_right = models.BooleanField(default=False)
    axle_str = models.BooleanField(default=False)
    axle_drv = models.BooleanField(default=False)
    axle_add = models.BooleanField(default=False)
    axle_trl = models.BooleanField(default=False)

    class Meta:
        ordering = ['part__part_type', 'part', 'truck', 'trailer', ]
        constraints = [
            models.UniqueConstraint(
                fields=['part', 'truck'], name='unique_truck_part'),
            models.UniqueConstraint(
                fields=['part', 'trailer'], name='unique_trailer_part'),
        ]

    @property
    def part_type(self):
        part_type = self.part.part_type.name
        if self.axle_str:
            part_type = part_type + ', STR'
        if self.axle_drv:
            part_type = part_type + ', DRV'
        if self.axle_add:
            part_type = part_type + ', ADD'
        if self.axle_trl:
            part_type = part_type + ', TRL'
        if self.side_left:
            part_type = part_type + ', L/S'
        if self.side_right:
            part_type = part_type + ', R/S'
        return part_type

    def __str__(self):
        try:
            part_type = self.part.part_type.name
            if self.axle_str:
                part_type = part_type + ', STR'
            if self.axle_drv:
                part_type = part_type + ', DRV'
            if self.axle_add:
                part_type = part_type + ', ADD'
            if self.axle_trl:
                part_type = part_type + ', TRL'
            if self.side_left:
                part_type = part_type + ', L/S'
            if self.side_right:
                part_type = part_type + ', R/S'
            if self.truck:
                name = part_type + ' for ' + self.truck.__str__()
            elif self.trailer:
                name = part_type + ' for ' + self.trailer.__str__()
        except AttributeError:
            name = 'Type not assigned'
        return name

    @property
    def is_unique(self):
        if self.side_left or self.side_right or self.axle_str or \
                self.axle_drv or self.axle_add or self.axle_trl:
            return False
        else:
            return True


class Shelf(models.Model):
    part = models.ManyToManyField(Part, blank=True)
    store = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name_plural = "shelves"
        # ordering = ['part__part__part_type', 'part']

    def __str__(self):
        return '#' + str(self.id) + ' ' + self.part.last().part_type.__str__()

    @property
    def in_stock(self):
        in_stock = 0
        for p in self.parts.all():
            in_stock += p.stock
        return in_stock


class Job(models.Model):
    name = models.CharField(max_length=50)
    man_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    part_types = models.ManyToManyField(PartType, blank=True)
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

    def __str__(self):
        return self.order.__str__() + ' ' + self.job.__str__()


class OrderPart(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        blank=True,
    )
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.order.__str__() + ' ' + self.part.__str__()


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
        return self.vendor.__str__() + ' ' + str(self.date)

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

    def __str__(self):
        return self.purchase + ' ' + self.part


class Mechanic(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return self.name if self.name else self.profile.user.first_name


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

    def __str__(self):
        return str(self.date) + ' ' + str(self.total)
