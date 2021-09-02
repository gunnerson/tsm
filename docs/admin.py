from django.contrib import admin

from .models import OrderImage, InspectionImage, TruckImage, TrailerImage, \
    TruckDocument, TrailerDocument, DriverDocument, CompanyDocument

admin.site.register(OrderImage)
admin.site.register(InspectionImage)
admin.site.register(TruckImage)
admin.site.register(TrailerImage)
admin.site.register(TruckDocument)
admin.site.register(TrailerDocument)
admin.site.register(DriverDocument)
admin.site.register(CompanyDocument)
