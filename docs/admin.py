from django.contrib import admin

from .models import TruckImage, TrailerImage, TruckDocument, TrailerDocument, \
    CompanyDocument

admin.site.register(TruckImage)
admin.site.register(TrailerImage)
admin.site.register(TruckDocument)
admin.site.register(TrailerDocument)
admin.site.register(CompanyDocument)
