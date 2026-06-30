from django.db import models


class Coupon(models.Model):
    DISCOUNT_CHOICES = (
        ('percent', 'Percent'),
        ('fixed', 'Fixed'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_CHOICES, default='percent')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    expires_at = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1)
    times_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
