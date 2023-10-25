from django import template
from product.models import Product

register = template.Library()


@register.inclusion_tag('partials/resent_products.html')
def resent_products(count=1):
    products = Product.objects.order_by('-created')[:count]
    return {'products': products}
