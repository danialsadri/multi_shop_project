from django import forms
from django.core import validators

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'validators': [validators.MaxValueValidator(100)]}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'validators': [validators.MaxValueValidator(500)]}),
        }
