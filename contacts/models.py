from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.core.validators import RegexValidator

from invent.models import Truck, Trailer
from users.models import Account
from invent.choices import company_group_choices


phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")


class Company(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    group = models.CharField(
        max_length=2,
        choices=company_group_choices(),
        default='GN',
    )
    name = models.CharField(max_length=20, unique=True)
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('contacts:update_company', args=[str(self.id)])


class Driver(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    truck = models.OneToOneField(
        Truck,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    trailer = models.OneToOneField(
        Trailer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=Q(group='OU') | Q(group='LO'),
    )
    phone_number = models.CharField(
        validators=[phone_number_regex],
        max_length=16,
        blank=True,
    )

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)

    def get_absolute_url(self):
        return reverse('contacts:update_driver', args=[str(self.id)])


class PasswordGroup(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=24, unique=True)
    comments = models.TextField()
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class PasswordAccount(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
    )
    group = models.ForeignKey(
        PasswordGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return str(self.name)


class PasswordRecord(models.Model):
    account = models.ForeignKey(
        PasswordAccount,
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=24)
    value = models.CharField(max_length=48)

    def __str__(self):
        return str(self.name)
