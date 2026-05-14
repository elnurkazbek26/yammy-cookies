from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, Product, Order

admin.site.site_header = 'Вкусняшки — Панель управления'
admin.site.site_title = 'Вкусняшки'
admin.site.index_title = 'Добро пожаловать в панель управления'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['position', 'name', 'slug', 'product_count']
    list_display_links = ['name']
    list_editable = ['position']
    ordering = ['position']
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['preview', 'name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']
    list_editable = ['price', 'is_available']
    search_fields = ['name', 'description']
    list_display_links = ['preview', 'name']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; width:50px; object-fit:cover; border-radius:8px;">',
                obj.image.url
            )
        return mark_safe('<span style="font-size:24px;">🍰</span>')
    preview.short_description = 'Фото'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'customer_name', 'phone', 'product', 'quantity', 'colored_total', 'status']
    list_filter = ['status', 'created_at', 'product__category']
    search_fields = ['customer_name', 'phone', 'email']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'product', 'customer_name', 'phone', 'email', 'address', 'quantity', 'comment']

    fieldsets = (
        ('Товар', {'fields': ('product', 'quantity')}),
        ('Клиент', {'fields': ('customer_name', 'phone', 'email')}),
        ('Доставка', {'fields': ('address', 'comment')}),
        ('Статус', {'fields': ('status', 'created_at')}),
    )

    def colored_status(self, obj):
        colors = {
            'new': '#2196F3',
            'processing': '#FF9800',
            'done': '#4CAF50',
            'cancelled': '#F44336',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:12px;">{}</span>',
            color, obj.get_status_display()
        )
    colored_status.short_description = 'Статус'

    def colored_total(self, obj):
        return format_html('<strong>{} тенге</strong>', obj.total_price())
    colored_total.short_description = 'Сумма'