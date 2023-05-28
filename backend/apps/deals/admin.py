from django.contrib import admin

from apps.deals.models import Image, Deal, Gallery, Offer, Review


class DealAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'worker', 'title', 'amount', 'start_time', 'deadline', 'status', 'created_at', ]
    list_display_links = ['id', 'owner', 'worker', ]
    list_filter = ['owner', 'worker']


class ImageInline(admin.TabularInline):
    model = Image


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'deal', 'title', ]
    list_display_links = ['id', 'deal']
    list_filter = ['deal', ]
    inlines = [ImageInline]


class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'worker', 'text', 'initiative']
    list_display_links = ['id', 'customer', 'worker', ]
    list_filter = ['customer', 'worker', ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'deal', 'text', 'is_answer']
    list_display_links = ['id', 'sender', 'deal', ]
    list_filter = ['sender', 'deal', ]


admin.site.register(Deal, DealAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Review, ReviewAdmin)
