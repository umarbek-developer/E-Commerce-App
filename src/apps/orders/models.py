from django.db import models
from django.conf import settings


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_address = models.ForeignKey('users.Address', null=True, blank=True, related_name='shipping_orders', on_delete=models.SET_NULL)
    billing_address = models.ForeignKey('users.Address', null=True, blank=True, related_name='billing_orders', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', related_name='order_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product}"


class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    provider = models.CharField(max_length=50, default='stripe')
    provider_payment_id = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for order {self.order_id}"


class Shipment(models.Model):
    order = models.OneToOneField(Order, related_name='shipment', on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='pending')
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipment {self.tracking_number or self.order_id}"
