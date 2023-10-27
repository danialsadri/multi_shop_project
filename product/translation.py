from modeltranslation.translator import TranslationOptions, register
from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['title', 'description']
