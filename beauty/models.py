from django.db import models


SERVICE_CHOICES = [
    ('hair_cut',      'Hair Cut'),
    ('hair_wash',     'Hair Wash'),
    ('luxury_facial', 'Luxury Facial'),
    ('manicure',      'Manicure'),
    ('pedicure',      'Pedicure'),
    ('hair_spa',      'Hair Spa'),
    ('waxing',        'Waxing'),
    ('henna',         'Henna'),
]

SERVICE_ICONS = {
    'hair_cut':      'fas fa-cut',
    'hair_wash':     'fas fa-shower',
    'luxury_facial': 'fas fa-spa',
    'manicure':      'fas fa-hand-sparkles',
    'pedicure':      'fas fa-shoe-prints',
    'hair_spa':      'fas fa-seedling',
    'waxing':        'fas fa-droplet',
    'henna':         'fas fa-paint-brush',
}


class BeautyPricing(models.Model):
    service = models.CharField(max_length=30, choices=SERVICE_CHOICES, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.get_service_display()

    @property
    def icon(self):
        return SERVICE_ICONS.get(self.service, 'fas fa-spa')

    class Meta:
        ordering = ['service']
        verbose_name = 'Beauty Pricing'
        verbose_name_plural = 'Beauty Pricing'
