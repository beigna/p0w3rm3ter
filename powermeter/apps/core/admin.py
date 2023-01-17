from django.contrib import admin

from core.models import Device, Metering


class DeviceAdmin(admin.ModelAdmin):
    pass


class MeteringAdmin(admin.ModelAdmin):
    pass


admin.site.register(Device, DeviceAdmin)
admin.site.register(Metering, MeteringAdmin)
