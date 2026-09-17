from django.db import models


SHOP_CHOICES = [
    ('mobile', 'Mobile Shop'),
    ('beauty', 'Beauty Parlour'),
    ('flower', 'Flower Shop'),
]


class HeroImage(models.Model):
    shop = models.CharField(max_length=20, choices=SHOP_CHOICES, unique=True)
    image = models.ImageField(upload_to='hero/')

    def __str__(self):
        return self.get_shop_display()

    class Meta:
        verbose_name = 'Hero Image'
        verbose_name_plural = 'Hero Images'


class BusinessImage(models.Model):
    shop = models.CharField(max_length=20, choices=SHOP_CHOICES, unique=True)
    image = models.ImageField(upload_to='business/')

    def __str__(self):
        return self.get_shop_display()

    class Meta:
        verbose_name = 'Business Image'
        verbose_name_plural = 'Business Images'


class MobileHeroBanner(models.Model):
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return 'Mobile Shop Hero Banner'

    def save(self, *args, **kwargs):
        # Keep only one record
        if not self.pk and MobileHeroBanner.objects.exists():
            MobileHeroBanner.objects.all().delete()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Mobile Hero Banner'
        verbose_name_plural = 'Mobile Hero Banner'
