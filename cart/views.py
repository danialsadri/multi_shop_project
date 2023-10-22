from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from cart.cart import Cart
from product.models import Product


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        size, color, quantity = request.POST.get('size', 'empty'), request.POST.get('color', 'empty'), request.POST.get('quantity', 'empty')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect('cart:detail')


class CartDeleteView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.delete(product_id)
        return redirect('cart:detail')
