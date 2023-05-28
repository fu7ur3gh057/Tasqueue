from django.contrib import admin

from apps.services.models import Service
from apps.workers.models import Worker, Image, Document, Gallery


class WorkerAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'full_name', 'root_services', 'documents_verified', 'rating', 'created_at']
    list_display_links = ['owner', 'full_name', ]
    list_filter = ['id', 'owner', ]

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def root_services(self, obj):
        result: list[Service] = []
        services: list[Service] = obj.services
        if services is None:
            return None
        for serv in services.all():
            if serv.is_root_node and serv not in result:
                result.append(serv)
        return result[:3]


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'name', ]
    list_display_links = ['id', 'owner', 'name', ]
    list_filter = ['owner', ]


class ImageInline(admin.TabularInline):
    model = Image


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'title', 'created_at']
    list_display_links = ['id', 'owner', ]
    list_filter = ['owner', ]
    inlines = [ImageInline]


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Gallery, GalleryAdmin)
