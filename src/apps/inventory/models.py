from django.db import models


class Stock(models.Model):
    variant = models.ForeignKey('catalog.ProductVariant', null=True, blank=True, related_name='stocks', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', null=True, blank=True, related_name='stocks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    warehouse = models.CharField(max_length=100, blank=True)
    reserved_quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'stocks'

    def __str__(self):
        return f"Stock for {self.product or self.variant}"


class StockMovement(models.Model):
    REASON_CHOICES = (
        ('sale', 'Sale'),
        ('restock', 'Restock'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
    )

    stock = models.ForeignKey(Stock, related_name='movements', on_delete=models.CASCADE)
    change_amount = models.IntegerField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, default='adjustment')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reason} ({self.change_amount})"
