from modeltranslation.translator import TranslationOptions, register
from .models import *


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['title', 'description']
