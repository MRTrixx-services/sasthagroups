# Create your models here.
from django.db import models
 
 
class ContactEnquiry(models.Model):
    """Stores every contact form submission from the Contact Us page."""
 
    SHOP_CHOICES = [
        ('mobile',  '📱 Mobile Shop'),
        ('parlour', '💄 Beauty Parlour'),
        ('flower',  '🌸 Flower Shop'),
        ('general', '🏪 All / General'),
    ]
 
    SUBJECT_CHOICES = [
        ('price_inquiry', 'Price Inquiry'),
        ('appointment',   'Book Appointment'),
        ('order',         'Place an Order'),
        ('complaint',     'Complaint / Feedback'),
        ('wholesale',     'Wholesale / Bulk'),
        ('other',         'Other'),
    ]
 
    # ── Fields ──
    name       = models.CharField(max_length=120, verbose_name='Customer Name')
    phone      = models.CharField(max_length=20,  verbose_name='WhatsApp Number')
    email      = models.EmailField(blank=True,    verbose_name='Email Address')
    shop       = models.CharField(max_length=20,  choices=SHOP_CHOICES, default='general', verbose_name='Shop')
    subject    = models.CharField(max_length=30,  choices=SUBJECT_CHOICES, verbose_name='Subject')
    message    = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Received At')
    is_read    = models.BooleanField(default=False, verbose_name='Read')
 
    class Meta:
        ordering         = ['-created_at']
        verbose_name     = 'Contact Enquiry'
        verbose_name_plural = 'Contact Enquiries'
 
    def __str__(self):
        return f"{self.name} ({self.get_shop_display()}) — {self.created_at.strftime('%d %b %Y %H:%M')}"
 