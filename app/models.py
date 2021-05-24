from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    sno=models.AutoField(primary_key=True,blank=False,null=False)
    name=models.CharField(max_length=100,blank=False,null=False)
    price=models.IntegerField(blank=False,null=False)
    desc=models.CharField(max_length=255,blank=False,null=False)
    img=models.ImageField(upload_to='media/product')
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    name=models.CharField(max_length=100,blank=False,null=False)
    price=models.IntegerField(blank=False,null=False)
    img=models.ImageField()

    def __str__(self):
        return self.name
    
class Suggestion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject =models.CharField(max_length=100,blank=False,null=False)
    message=models.CharField(max_length=100,blank=False,null=False)
    
    def __str__(self):
        return self.user