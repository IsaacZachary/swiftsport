from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, ShopSettings


def thumb(url, size=64):
    return format_html('<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:6px">', url, size, size)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('preview', 'image', 'order')
    readonly_fields = ('preview',)

    @admin.display(description='Photo')
    def preview(self, obj):
        return thumb(obj.image.url, 80) if obj.pk and obj.image else '—'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('cover', 'name', 'category', 'price', 'price_max', 'in_stock')
    list_display_links = ('cover', 'name')
    list_editable = ('price', 'price_max', 'in_stock')
    list_filter = ('category', 'in_stock')
    search_fields = ('name', 'description')
    fields = ('name', 'category', 'price', 'price_max', 'description', 'in_stock', 'order')
    inlines = [ProductImageInline]
    list_per_page = 50

    @admin.display(description='')
    def cover(self, obj):
        first = obj.images.first()
        return thumb(first.image.url) if first else '—'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ShopSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
