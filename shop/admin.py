from django.contrib import admin

from .models import Order, Part, Job, OrderJob, OrderPart, Purchase, \
    PurchaseItem, Mechanic, Balance

admin.site.register(Order)
admin.site.register(Part)
admin.site.register(Job)
admin.site.register(OrderJob)
admin.site.register(OrderPart)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(Mechanic)
admin.site.register(Balance)
