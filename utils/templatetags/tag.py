from django import template
from django.db.models import Count

from product.models import Product

register = template.Library()


@register.inclusion_tag('partials/resent_products.html')
def resent_products(count=1):
    products = Product.objects.order_by('-created')[:count]
    return {'products': products}


@register.simple_tag()
def popular_products(count=1):
    return Product.objects.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]
