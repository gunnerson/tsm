from django.contrib import admin

from .models import Truck, Trailer, Company

admin.site.register(Truck)
admin.site.register(Trailer)
admin.site.register(Company)
