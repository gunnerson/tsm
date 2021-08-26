from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

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
