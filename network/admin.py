from django.contrib import admin
from .models import Contact, Product, NetworkNode

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'country', 'city']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'release_date']

@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier', 'get_level', 'debt', 'created_at']

    def get_level(self, obj):
        return obj.level

    get_level.short_description = 'Level'