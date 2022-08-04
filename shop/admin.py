from django.contrib import admin

from .models import Order, OrderTime, Part, Job, OrderJob, OrderPart, \
    Purchase, PurchaseItem, Mechanic, Balance, PartType, PartPlace, Shelf, \
    ShelfGroup

admin.site.register(Order)
admin.site.register(OrderTime)
admin.site.register(Part)
admin.site.register(PartType)
admin.site.register(Job)
admin.site.register(OrderJob)
admin.site.register(OrderPart)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(Mechanic)
admin.site.register(Balance)
admin.site.register(PartPlace)
admin.site.register(Shelf)
admin.site.register(ShelfGroup)
