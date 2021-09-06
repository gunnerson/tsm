from django.contrib import admin

from .models import Truck, Trailer, Driver, Company, PasswordGroup, \
    PasswordAccount, PasswordRecord

admin.site.register(Truck)
admin.site.register(Trailer)
admin.site.register(Driver)
admin.site.register(Company)
# admin.site.register(PasswordGroup)
# admin.site.register(PasswordAccount)
# admin.site.register(PasswordRecord)
