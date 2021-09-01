from django.contrib import admin

from .models import OrderImage, InspectionImage, TruckImage, TrailerImage

admin.site.register(OrderImage)
admin.site.register(InspectionImage)
admin.site.register(TruckImage)
admin.site.register(TrailerImage)
