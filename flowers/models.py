from django.db import models


class FlowerPricing(models.Model):
    UNIT_CHOICES = [
        ('metre',   '/ metre'),
        ('onwards', 'onwards'),
        ('dozen',   '/ dozen'),
        ('string',  '/ string'),
        ('day',     '/ day'),
        ('set',     '/ set'),
    ]

    slug  = models.SlugField(unique=True)
    price = models.PositiveIntegerField()
    unit  = models.CharField(max_length=10, choices=UNIT_CHOICES)

    def __str__(self):
        return f"{self.slug} – ₹{self.price} {self.unit}"

    class Meta:
        verbose_name_plural = 'Flower Pricing'
