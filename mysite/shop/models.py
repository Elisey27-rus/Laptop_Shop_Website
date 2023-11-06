from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


def product_image_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/image/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_category = models.ForeignKey(Category, on_delete=models.PROTECT)
    product_description = models.TextField()
    product_discount = models.IntegerField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=1)
    product_image = models.ImageField(null=True, blank=True, upload_to=product_image_path)

    def __str__(self):
        return self.product_name


def profile_image_path(instance: "User_profile", filename: str) -> str:
    return "profile/image".format(
        filename=filename
    )


class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birthday = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to=profile_image_path)
    GENDER_CHOICES = [
        ('M', 'Муж'),
        ('F', 'Жен'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    city = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
