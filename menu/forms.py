from django import forms
from django.utils import timezone

from .models import Menu


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
            'expiration_date'
        ]

    def clean_expiration(self):
        expiration_date_key = self.cleaned_data['expiration_date']
        if expiration_date_key < timezone.now().date():
            raise forms.ValidationError("Enter a date that is later than today!")
        return expiration_date_key
