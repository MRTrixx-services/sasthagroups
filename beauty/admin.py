from django.contrib import admin
from .models import BeautyPricing


@admin.register(BeautyPricing)
class BeautyPricingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price')
    list_display_links = ('__str__',)
    list_editable = ('price',)
