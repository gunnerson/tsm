from django.contrib import admin

from contacts.models import Company, Driver, PasswordGroup

admin.site.register(Company)
admin.site.register(Driver)
admin.site.register(PasswordGroup)
