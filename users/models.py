from django.db import models
from datetime import date
from django.contrib.auth.models import User


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
        return str(self.profile) + '_' + self.list_name + '_' + self.field_name

    class Meta:
        verbose_name_plural = 'ListColShows'
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'list_name', 'field_name'],
                name='unique_listcolshow',
            ),
        ]
        ordering = ['profile', '-list_name', 'id']
