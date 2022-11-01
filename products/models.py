from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category_image/", blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='images/')
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
