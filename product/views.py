from django.shortcuts import render
from django.views import View


class ProductListView(View):
    def get(self, request):
        return render(request, 'product/product_list.html', {})
