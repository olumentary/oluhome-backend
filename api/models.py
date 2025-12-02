from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Vendor(models.Model):
    # Vendor model for managing vendor information
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vendors',
        help_text="The user who owns this vendor"
    )
    vendor_name = models.CharField(
        max_length=255,
        help_text="Name of the vendor"
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Vendor's address"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Vendor's phone number"
    )
    email_address = models.EmailField(
        blank=True,
        null=True,
        help_text="Vendor's email address"
    )
    website = models.URLField(
        blank=True,
        null=True,
        help_text="Vendor's website URL"
    )
    primary_contact_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of the primary contact person"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vendors'
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.vendor_name
