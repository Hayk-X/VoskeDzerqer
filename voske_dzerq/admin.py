from django.contrib import admin
from .models import MenuItem, Order

# Մոդելների գրանցում

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_hy', 'name_ru', 'name_en', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'name_hy', 'name_ru', 'name_en', 'description', 'description_hy', 'description_ru', 'description_en')
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'price', 'image', 'is_available')
        }),
        ('Armenian', {
            'fields': ('name_hy', 'description_hy')
        }),
        ('Russian', {
            'fields': ('name_ru', 'description_ru')
        }),
        ('English', {
            'fields': ('name_en', 'description_en')
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'total_price', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('customer_name', 'phone', 'order_details')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
