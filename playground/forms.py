from django import forms
from .models import Films_Cost, TEST_Like_films
from django.forms import ModelForm, TextInput, NumberInput

class Like_filmsForm(ModelForm):
    class Meta:
        model = TEST_Like_films
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

class InputForm(forms.Form):
    my_input = forms.CharField(label='my_input', max_length=100)


class FilmsCostForm(forms.ModelForm):
    class Meta:
        model = Films_Cost
        fields = ['cost', 'viewing_method', 'quality']

