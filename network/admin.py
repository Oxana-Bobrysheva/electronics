from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, Product, NetworkNode


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'country', 'city']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'release_date']


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier_link', 'get_level', 'debt', 'created_at']
    list_filter = ['contact__city']
    actions = ['clear_debt']
    search_fields = ['name']

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html('<a href="{}">{}</a>',
                               f'../networknode/{obj.supplier.id}/',
                               obj.supplier.name)
        return "-"

    supplier_link.short_description = 'Supplier'

    def get_level(self, obj):
        return obj.level

    get_level.short_description = 'Level'

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена у {updated} объектов")

    clear_debt.short_description = "Очистить задолженность у выбранных объектов"
