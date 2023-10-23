from django.db import models
from accounts.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.PositiveBigIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    quantity = models.PositiveBigIntegerField()
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return self.order.user.phone_number
