from django.contrib import admin
from .models import ContactEnquiry

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'shop', 'subject', 'created_at', 'is_read')
    list_filter   = ('shop', 'subject', 'is_read')
    search_fields = ('name', 'phone', 'email', 'message')
    ordering      = ('-created_at',)
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)