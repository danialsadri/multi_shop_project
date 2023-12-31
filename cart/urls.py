from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('detail/', views.CartDetailView.as_view(), name='detail'),
    path('add/<int:product_id>', views.CartAddView.as_view(), name='add'),
    path('delete/<str:product_id>', views.CartDeleteView.as_view(), name='delete'),
    path('order/detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('apply/discount/<int:order_id>/', views.ApplyDiscountView.as_view(), name='apply_discount'),
    path('request/<int:order_id>/', views.SendRequestView.as_view(), name='request'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
]
