from django import forms
from django.core.exceptions import ValidationError
from . import models

class ContactForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'classe-a classe-b',
                'placeholder': 'Seu nome aqui',
            }
        ),
        label = 'Primeiro Nome',
        help_text='Texto de ajuda',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone', 'email',
        )

def clean(self):
    #cleaned_data = self.cleaned_data

    self.add_error(
        'first_name',
        ValidationError(
            'Mensagem de erro',
            code='invalid'
        )
    )

    return super().clean()