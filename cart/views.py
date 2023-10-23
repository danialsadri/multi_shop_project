from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from cart.cart import Cart
from cart.models import Order, OrderItem, DiscountCode
from product.models import Product


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        size, color, quantity = request.POST.get('size', 'empty'), request.POST.get('color', 'empty'), request.POST.get(
            'quantity', 'empty')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect('cart:detail')


class CartDeleteView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.delete(product_id)
        return redirect('cart:detail')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'cart/order_detail.html', {'order': order})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=int(cart.total()))
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], size=item['size'], color=item['color'],
                                     quantity=item['quantity'], price=item['price'])
        cart.remove_cart()
        return redirect('cart:order_detail', order.id)


class ApplyDiscountView(View):
    def post(self, request, order_id):
        code = request.POST.get('code')
        order = get_object_or_404(Order, id=order_id)
        discount_code = get_object_or_404(DiscountCode, name=code)
        if discount_code.quantity == 0:
            return redirect('cart:order_detail', order.id)
        order.total_price -= order.total_price * discount_code.discount / 100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('cart:order_detail', order.id)
