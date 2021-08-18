from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User

from .utils import gen_list_ver_name, gen_field_ver_name
from invent.choices import size_choices



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(
        'Account',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return str(self.user.username)


class Account(models.Model):
    name = models.CharField(max_length=24)
    expiration_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.name)

    def is_active(self):
        return self.expiration_date >= date.today()


class ListColShow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=18)
    field_name = models.CharField(max_length=18)
    show = models.BooleanField(default=True)

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
        ordering = ['profile', '-list_name', 'id']


class PreferenceList(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    trucks_font = models.CharField(
        max_length=1,
        choices=size_choices(),
        default='M',
        verbose_name='Trucks List Font Size'
    )

    def __str__(self):
        return str(self.profile)

    def get_absolute_url(self):
        return reverse('users:preferences', args=[str(self.id)])
