from django.db import models
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('contacts:update_company', args=[str(self.id)])


class Driver(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.first_name + self.last_name)

    def get_absolute_url(self):
        return reverse('contacts:update_driver', args=[str(self.id)])
