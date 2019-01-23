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

        widgets = {'created_date': forms.HiddenInput()}

    def clean_expiration_dat(self):
        expiration_date_key = self.cleaned_data.get['expiration_date']
        if expiration_date_key < timezone.now().date():
            raise forms.ValidationError("Enter a date that is later than today!")
        return expiration_date_key
