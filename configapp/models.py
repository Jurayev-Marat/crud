from django.db import models
from decimal import Decimal

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"

class Suppliers(models.Model):
    company_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_title = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "Suppliers"

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

class Order_details(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} ta"

    class Meta:
        verbose_name_plural = "Order Details"

class Orders(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField()
    order_dtls = models.ForeignKey(Order_details, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id} - {self.order_date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "Orders"