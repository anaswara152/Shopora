from django.db import models
from django.contrib.auth.models import User
from siteadmin.models import Product
# Create your models here.
class reg(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    city=models.CharField(max_length=100)
    postalcode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    phone=models.CharField(max_length=100,null=True,blank=True)
    
    
    
class whislist(models.Model):
    customerid=models.ForeignKey(User,on_delete=models.CASCADE)
    productid=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    
class cart(models.Model):
    customerid=models.ForeignKey(User,on_delete=models.CASCADE)
    productid=models.ForeignKey(Product,on_delete=models.CASCADE)
    count=models.IntegerField()
    price=models.IntegerField()
    
    
    
    
class Order(models.Model):
    
    PAYMENT_CHOICES = (
        ('COD', 'Cash On Delivery'),
        ('UPI', 'UPI'),
        ('CARD', 'Credit/Debit Card'),
    )

    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )

    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    total_price = models.FloatField()

    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')

    order_status = models.CharField(max_length=15, choices=ORDER_STATUS, default='PENDING')

    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    carrier=models.CharField(max_length=100,null=True,blank=True)
    tracking=models.CharField(max_length=100,null=True,blank=True)
    shipping_date=models.CharField(max_length=100,null=True,blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.order.id} - {self.product.name}"