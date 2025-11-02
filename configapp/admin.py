from django.contrib import admin
from .models import Category, Product, Suppliers, Order_details, Orders


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'description']
    search_fields = ['category_name']
    list_per_page = 20


@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_name', 'city', 'phone']
    search_fields = ['company_name', 'contact_name']
    list_filter = ['city', 'country']
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'unit_price', 'category', 'suppliers', 'display_photo']
    list_filter = ['category', 'suppliers']
    search_fields = ['product_name']
    list_per_page = 20

    def display_photo(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit: cover;" />'
        return "No photo"

    display_photo.allow_tags = True
    display_photo.short_description = 'Rasm'


@admin.register(Order_details)
class Order_detailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'unit_price', 'quantity', 'total_price']
    list_filter = ['product']
    list_per_page = 20


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_date', 'required_date', 'order_dtls']
    list_filter = ['order_date']
    date_hierarchy = 'order_date'
    list_per_page = 20