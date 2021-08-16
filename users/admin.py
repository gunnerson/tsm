from django.contrib import admin

from .models import Profile, Account, ListColShow, PreferenceList

admin.site.register(Profile)
admin.site.register(Account)
admin.site.register(PreferenceList)
admin.site.register(ListColShow)

