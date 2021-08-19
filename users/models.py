from django.db import models
from django.conf import settings
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from .utils import gen_list_ver_name, gen_field_ver_name
from invent.choices import size_choices, level


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email.split("@")[0]


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(
        'Account',
        on_delete=models.SET_NULL,
        null=True
    )
    level = models.CharField(
        max_length=1,
        choices=level(),
        default='N',
    )

    def __str__(self):
        return str(self.user)


class Account(models.Model):
    name = models.CharField(max_length=36)
    expiration_date = models.DateField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        d = date.today()
        try:
            self.expiration_date = d.replace(year=d.year + 1)
        except ValueError:
            self.expiration_date = d + (date(d.year + 1, 1, 1) -
                                        date(d.year, 1, 1))
        super(Account, self).save(*args, **kwargs)

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
    font_size = models.CharField(
        max_length=1,
        choices=size_choices(),
        default='M',
    )

    def __str__(self):
        return str(self.profile)

    def get_absolute_url(self):
        return reverse('users:preferences', args=[str(self.id)])
