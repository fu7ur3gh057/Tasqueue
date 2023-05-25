from django.contrib import admin

from apps.categories.models import Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'default_price']
    list_display_links = ['id', 'name', 'parent',]
#    list_filter = ['id', 'owner', 'city', ]


admin.site.register(Category, CategoryAdmin)
