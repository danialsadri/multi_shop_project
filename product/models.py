from django.db import models
from datetime import datetime
from django.utils.html import format_html


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs', blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


def get_image_product(instance, filename):
    return f"product_images/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to=get_image_product)
    price = models.PositiveSmallIntegerField()
    discount = models.PositiveSmallIntegerField()
    size = models.ManyToManyField(Size, related_name='products')
    color = models.ManyToManyField(Color, related_name='products')

    def __str__(self):
        return self.title

    def get_image(self):
        return format_html(f"<img src='{self.image.url}' alt='{self.title}' width='70px' height='50px'>")


class Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='informations', blank=True, null=True)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.text[20]
