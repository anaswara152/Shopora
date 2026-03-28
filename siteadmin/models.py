from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class category(models.Model):
    cname=models.CharField(max_length=100)

    def __str__(self):
        return self.cname
   
def validate_jpg(value):
    if not value.name.lower().endswith('.jpg'):
        raise ValidationError('Only JPG images are allowed.')
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=100,null=True,blank=True)
    fabric = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.FloatField()   
    stock_quantity = models.PositiveIntegerField() 
    categoryid = models.ForeignKey(category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', validators=[validate_jpg],null=True, blank=True)
    def __str__(self):
        return self.name
    
    
    