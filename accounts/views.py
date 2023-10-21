from random import randint
from uuid import uuid4
import ghasedakpack
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import OtpLoginForm, CheckOtpForm, AddressForm
from .models import Otp, User
import requests

SMS = ghasedakpack.Ghasedak("246e7e90df21bb4a5bcba2122aaeae50cf68b3f31e4832b6112b99f15e32a135")


class OtpLoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = OtpLoginForm()
        return render(request, 'accounts/otp_login.html', {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = randint(1000, 9999)
            print(random_code)
            # SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'multishop', 'param1': random_code})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=random_code, token=token)
            return redirect(reverse('accounts:check_otp') + f"?token={token}")
        return render(request, 'accounts/otp_login.html', {'form': form})


class CheckOtpView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'accounts/check_otp.html', {'form': form})

    def post(self, request):
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            token = request.GET.get('token')
            if Otp.objects.filter(code=code, token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone_number=otp.phone)
                login(request, user)
                otp.delete()
                return redirect('home:home')
        return render(request, 'accounts/check_otp.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')


class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'accounts/address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('home:home')
        return render(request, 'accounts/address.html', {'form': form})
