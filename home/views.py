from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render
from django.views import View

from product.models import Product, Category
from .forms import SearchForm


class HomeView(View):
    def get(self, request):
        product = Product.objects.last()
        categories = Category.objects.all()
        return render(request, 'home/home.html', {'product': product, 'categories': categories})


class SearchView(View):
    def get(self, request):
        query = None
        results = []
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data.get('query')
                results1 = Product.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1)
                results2 = Product.objects.annotate(similarity=TrigramSimilarity('description', query)).filter(similarity__gt=0.1)
                results = (results1 | results2).order_by('-similarity')
        return render(request, 'home/search.html', {'query': query, 'results': results})
