from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('list/', views.ProductListView.as_view(), name='list'),
    path('list/<str:category>/', views.ProductListView.as_view(), name='list_category'),
    path('detail/<int:product_id>/', views.ProductDetailView.as_view(), name='detail'),
    path('header/', views.HeaderPartialView.as_view(), name='header'),
]
