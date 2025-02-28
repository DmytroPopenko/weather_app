from .models import Weather
from django.forms import ModelForm, TextInput, DateField, CharField


class WeatherForm(ModelForm):
    class Meta:
        model = Weather
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={
                'id': 'name_input',
                'name': 'name_input',
                'list': "names",
                'class': 'form-control',
                'placeholder': 'City name'
            })
        }
