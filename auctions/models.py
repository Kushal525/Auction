from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime

class User(AbstractUser):
    address = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^[7-9]\d{9}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False) # validators should be a list


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="departures")
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255)
    product_price = models.IntegerField()
    product_img = models.ImageField(upload_to=None, blank=True)
    product_created_on = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return f"{self.id} {self.user} {self.product_name} {self.product_category} {self.product_price} {self.product_img} {self.product_created_on}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_comment")
    comment = models.CharField(max_length=20)
    comment_on = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return f"{self.id} {self.user} {self.product} {self.comment} {self.comment_on}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    product = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE, related_name="product_watchlist")

    def __str__(self):
        return f"{self.user} {self.product}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_bid")
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.user} {self.product} {self.amount}"


