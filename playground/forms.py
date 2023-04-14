from .models import Like_films
from django.forms import ModelForm, TextInput, NumberInput

class Like_filmsForm(ModelForm):
    class Meta:
        model = Like_films
        fields = ["name","cost","rent"]
        widgets = {
            "name":TextInput(attrs={
            'class':'form-control',
            'placeholder':'Введи текст'
            }),
            "cost":NumberInput(attrs={
            'class':'form-control',
            'placeholder':'Введи cost'
            }),
            "rent":NumberInput(attrs={
            'class':'form-control',
            'placeholder':'Введи rent'
            })
        }