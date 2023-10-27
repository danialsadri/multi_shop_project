from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from django.core.exceptions import ValidationError
from .models import User, Address, ContactUs
from django.utils.text import gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["phone_number"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"), help_text="you can change password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ["phone_number", "password", "is_active", "is_admin", 'last_login']


class OtpLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            validators=[validators.MaxLengthValidator(11)], label=_("phone_number"))


class CheckOtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           validators=[validators.MaxLengthValidator(4)], label=_("code"))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'validators': [validators.MaxLengthValidator(100)]}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'validators': [validators.MaxLengthValidator(100)]}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'validators': [validators.MaxLengthValidator(11)]}),
            'subject': forms.TextInput(
                attrs={'class': 'form-control', 'validators': [validators.MaxLengthValidator(100)]}),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'validators': [validators.MaxLengthValidator(500)]}),
        }
