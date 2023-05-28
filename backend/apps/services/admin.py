from django.contrib import admin

from apps.services.models import Service


# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'default_price']
    list_display_links = ['id', 'name', 'parent',]
#    list_filter = ['id', 'owner', 'city', ]


admin.site.register(Service, ServiceAdmin)
