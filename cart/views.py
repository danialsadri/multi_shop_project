from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from accounts.models import Address
from cart.cart import Cart
from cart.models import Order, OrderItem, DiscountCode
from product.models import Product
from django.conf import settings
import requests
import json


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


class ApplyDiscountView(LoginRequiredMixin, View):
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


class SendRequestView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(klass=Order, id=order_id, user=request.user)
        address = get_object_or_404(klass=Address, id=request.POST.get('address'))
        order.address = f"{address.address}---{address.phone}"
        order.save()
        request.session['order_id'] = str(order.id)
        data = {"MerchantID": settings.MERCHANT, "Amount": order.total_price, "Description": settings.description,
                "Phone": request.user.phone_number, "CallbackURL": settings.CallbackURL}
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']),
                            'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


class VerifyView(LoginRequiredMixin, View):
    def get(self, request, authority):
        order_id = request.session['order_id']
        order = get_object_or_404(klass=Order, id=int(order_id))
        data = {"MerchantID": settings.MERCHANT, "Amount": order.total_price, "Authority": authority}
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                order.is_paid = True
                order.save()
                return {'status': True, 'RefID': response['RefID']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response
