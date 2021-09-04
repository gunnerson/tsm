from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from invent.models import Company
from .utils import gen_list_ver_name, gen_field_ver_name
from .managers import UserManager
from invent.choices import size_choices, level


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email.split("@")[0]


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    level = models.CharField(
        max_length=1,
        choices=level(),
        default='N',
    )
    font_size = models.CharField(
        max_length=1,
        choices=size_choices(),
        default='M',
    )
    labor_rate = models.PositiveSmallIntegerField(default=100)
    parts_surcharge = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.1,
    )
    tax = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.1,
    )
    shop_header = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'group': 'OU'},
    )
    home_latitude = models.FloatField(default=42.0203018)
    home_longitude = models.FloatField(default=-88.318316)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('users:profile', args=[str(self.id)])


class ListColShow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=24)
    field_name = models.CharField(max_length=24)
    show = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return gen_list_ver_name(self.list_name) + ' | ' + \
            gen_field_ver_name(self.field_name)

    class Meta:
        verbose_name_plural = 'ListColShows'
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'list_name', 'field_name'],
                name='unique_listcolshow',
            ),
        ]
        ordering = ['profile', '-list_name', 'order']


class PunchCard(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    punch_in = models.DateTimeField(null=True)
    punch_in_distance = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=1,
    )
    lunch_in = models.DateTimeField(null=True, blank=True)
    lunch_in_distance = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=1,
    )
    lunch_out = models.DateTimeField(null=True, blank=True)
    lunch_out_distance = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=1,
    )
    punch_out = models.DateTimeField(null=True, blank=True)
    punch_out_distance = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=1,
    )
