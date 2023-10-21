from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.OtpLoginView.as_view(), name='login'),
    path('check_otp/', views.CheckOtpView.as_view(), name='check_otp'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('address/', views.AddressView.as_view(), name='address'),
]
