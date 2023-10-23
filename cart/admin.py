from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    classes = ['collapse']
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'is_paid', 'created']
    list_filter = ['is_paid', 'created']
    search_fields = ['user']
    raw_id_fields = ['user']
    inlines = [OrderItemInline]
