from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    # Admin configuration for Vendor model
    list_display = ('vendor_name', 'user', 'phone_number', 'email_address', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('vendor_name', 'email_address', 'primary_contact_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'vendor_name', 'primary_contact_name')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone_number', 'email_address', 'website')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
