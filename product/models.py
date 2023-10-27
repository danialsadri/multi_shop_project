from datetime import datetime
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs', blank=True, null=True, verbose_name=_('parent'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))

    class Meta:
        verbose_name = _('size')
        verbose_name_plural = _('sizes')

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')

    def __str__(self):
        return self.title


def get_image_product(instance, filename):
    return f"product_images/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products', blank=True, verbose_name=_('category'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(max_length=500, verbose_name=_('description'))
    image = models.ImageField(upload_to=get_image_product, verbose_name=_('image'))
    price = models.PositiveSmallIntegerField(verbose_name=_('price'))
    discount = models.PositiveSmallIntegerField(verbose_name=_('discount'))
    size = models.ManyToManyField(Size, related_name='products', verbose_name=_('size'))
    color = models.ManyToManyField(Color, related_name='products', verbose_name=_('color'))
    created = models.DateTimeField(default=timezone.now, verbose_name=_('created'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title

    def get_image(self):
        return format_html(f"<img src='{self.image.url}' alt='{self.title}' width='70px' height='50px'>")

    def get_absolute_url(self):
        return reverse(viewname='product:detail', kwargs={'product_id': self.id})


class Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='informations', blank=True, null=True, verbose_name=_('product'))
    text = models.TextField(max_length=500, verbose_name=_('text'))

    class Meta:
        verbose_name = _('information')
        verbose_name_plural = _('informations')

    def __str__(self):
        return self.text[20]


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('product'))
    name = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(max_length=500, verbose_name=_('description'))
    active = models.BooleanField(default=False, verbose_name=_('active'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return self.name
