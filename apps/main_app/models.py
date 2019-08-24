from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return f"<Fname: {self.first_name}>"

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    photo = models.FileField(upload_to='products/photos/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<ID: {self.id}, Prod Name: {self.product_name}>"

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)




class Order(models.Model):
    quantity_ordered = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"< Order ID: {self.id}, Total: ${self.total_price}>"