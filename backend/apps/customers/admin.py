from django.contrib import admin

from apps.customers.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'full_name', 'city', 'created_at']
    list_display_links = ['owner', 'full_name', 'city', ]
    list_filter = ['id', 'owner', 'city', ]

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


admin.site.register(Customer, CustomerAdmin)
