from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register custom user
UserAdmin.fieldsets += ('Custom fields set', {'fields': ('address', 'role')}),
admin.site.register(User, UserAdmin)

# Register necessary sizakat model
admin.site.register(Period)
admin.site.register(ZakatType)

# For dev
admin.site.register(Muzakki)
admin.site.register(ZakatQuality)
admin.site.register(ZakatPayment)
admin.site.register(ZakatTransaction)
