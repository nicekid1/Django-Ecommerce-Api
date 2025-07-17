from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock')
    list_filter = ('category',)
    search_fields = ('title', 'description')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_paid', 'payment_status')
    list_filter = ('is_paid',)
    search_fields = ('user__email',)
    inlines = [OrderItemInline]
    readonly_fields = ('payment_status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'authority', 'ref_id', 'status', 'created_at')
    search_fields = ('user__email', 'order__id', 'authority', 'ref_id')
    readonly_fields = ('user', 'order', 'amount', 'authority', 'ref_id', 'status', 'created_at')