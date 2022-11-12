from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('categories')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse('products')

    def __str__(self):
        return self.name

class Basket(models.Model):
    number = models.IntegerField()
    products = models.ManyToManyField(Product)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Savat"

    def __str__(self):
        return f"{self.number}"