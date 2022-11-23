from django.db import models
from django.shortcuts import reverse

from django.conf import settings


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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse('products')

    def get_add_to_card_url(self):
        return reverse('add_to_card', kwargs={
            'id': self.id
        })

    def get_remove_from_card_url(self):
        return reverse('remove_from_card', kwargs={
            'id': self.id
        })

    def __str__(self):
        return self.name

class OrderProduct(models.Model):
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_product_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_product_discount_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_product_discount_price()
        return self.get_total_product_price()


class Order(models.Model):
    ref_code = models.IntegerField()
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_completed = models.BooleanField(default=False)
    order_completed_date = models.DateTimeField(null=True, blank=True)
    cash = models.IntegerField()
    plastic = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Buyurtma raqami-{self.ref_code}, sana:{self.ordered_date.day}-{self.ordered_date.month}-{self.ordered_date.year}'

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total

    def get_order_price(self):
        if self.plastic:
            return self.cash + self.plastic
        else:
            return self.cash

    def get_products_ordered_url(self):
        return reverse('products_ordered', kwargs={
            'ref_code': self.ref_code
        })

    def get_partial_payment_url(self):
        return reverse('partial_payment', kwargs={
            'pk': self.pk
        })

    def get_absolute_url(self):
        if self.plastic:
            if self.get_total() == (self.plastic + self.cash):
                return reverse('products_ordered', kwargs={
                    'ref_code': self.ref_code
                })
            else:
                return reverse('partial_payment', kwargs={
                    'pk': self.pk
                })
        else:
            return reverse('products_ordered', kwargs={
                'ref_code': self.ref_code
            })

    def get_order_completed_url(self):
        return reverse('order_completed', kwargs={
            'ref_code': self.ref_code
        })