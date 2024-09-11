from django.contrib import admin
from .models import *

class PartOptionInline(admin.TabularInline):
    model = PartOption
    extra = 1

class PartTypeInline(admin.TabularInline):
    model = PartType
    extra = 1
    inlines = [PartOptionInline]

class ProductAdmin(admin.ModelAdmin):
    inlines = [PartTypeInline]
    list_display = ('name', 'category', 'base_price')
    list_filter = ('category',)
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'selected_options', 'quantity', 'price')

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'session_key', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)

class IncompatibilityAdmin(admin.ModelAdmin):
    list_display = ('part_option_1', 'part_option_2')

class PriceRuleAdmin(admin.ModelAdmin):
    filter_horizontal = ('part_options',)
    list_display = ('id', 'price_adjustment')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(PartType)
admin.site.register(PartOption)
admin.site.register(Incompatibility, IncompatibilityAdmin)
admin.site.register(PriceRule, PriceRuleAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)