from django.contrib import admin

from .models import Order, Part, PartAmount, Job, JobItem, Purchase, PurchaseItem

admin.site.register(Order)
admin.site.register(Part)
admin.site.register(PartAmount)
admin.site.register(Job)
admin.site.register(JobItem)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
