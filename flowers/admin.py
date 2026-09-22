from django.contrib import admin
from .models import FlowerPricing


@admin.register(FlowerPricing)
class FlowerPricingAdmin(admin.ModelAdmin):
    list_display = ('slug', 'price', 'unit')
