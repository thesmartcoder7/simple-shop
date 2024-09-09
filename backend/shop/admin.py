from django.contrib import admin
from .models import *

# Inline for VariationOption within VariationType
class VariationOptionInline(admin.TabularInline):  # or StackedInline for a different layout
    model = VariationOption
    extra = 1  # Number of extra blank rows for new options
    min_num = 1  # Ensures at least one option is present
    fields = ['option_name', 'price_change']  # Fields to display for each option

# VariationType Admin with Inline for VariationOption
@admin.register(VariationType)
class VariationTypeAdmin(admin.ModelAdmin):
    inlines = [VariationOptionInline]
    list_display = ['variation_name']  # Displays the variation type name
    search_fields = ['variation_name']  # Allows searching for variation types by name

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(VariationOption)
admin.site.register(ProductItem)
admin.site.register(ProductVariation)

