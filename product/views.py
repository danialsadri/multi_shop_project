from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Product, Category


class ProductListView(View):
    def get(self, request, category=None):
        # filter by size color min price max price
        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        products = Product.objects.all()
        if colors:
            products = products.filter(color__title__in=colors).distinct()
        if sizes:
            products = products.filter(size__title__in=sizes).distinct()
        if min_price and max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)
        # category
        if category is not None:
            products = Product.objects.filter(category__title=category)
        else:
            products = Product.objects.all()
        # pagination
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page', 1)
        try:
            products = paginator.page(page_number)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            products = paginator.page(1)
        return render(request, 'product/product_list.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        comments = product.comments.filter(active=True)
        form = CommentForm()
        context = {'product': product, 'comments': comments, 'form': form}
        return render(request, 'product/product_detail.html', context)


class HeaderPartialView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'partials/header.html', {'categories': categories})


class CommentView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        comment = None
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
        context = {'product': product, 'comment': comment, 'form': form}
        return render(request, 'product/comment.html', context)
