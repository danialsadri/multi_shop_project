from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View
from product.models import Product


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page', 1)
        try:
            products = paginator.page(page_number)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            products = paginator.page(1)
        return render(request, 'product/product_list.html', {'products': products})
