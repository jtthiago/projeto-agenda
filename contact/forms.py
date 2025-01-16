from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class ContactForm(forms.ModelForm):


    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'classe-a classe-b',
                'placeholder': 'Aqui veio do init',
                'accept': 'image/*',
            }
        ),
        label='Primeiro Nome',
        help_text='Texto de ajuda para seu usuário',
        )
    

    

    
    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'description', 'category', 'picture',
            
        )

    def clean(self):
        # Obtendo os dados limpos
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        # Verificando se `first_name` é igual a `last_name`
        if first_name == last_name:
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        # Retornando os dados limpos
        return super().clean()

class RegisterForm(UserCreationForm):
    first_name = forms.CharField( min_length=3, required=True)
    last_name = forms.CharField( min_length=3, required=True)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1',
            'password2',
        )

    def clean_email(self):
        
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Esse email já existe', code='invalid')
            )
            
        return email

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhar não batem')
                )
        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'eamil',
                    ValidationError('Já existe este e-mail', code='invalid')
                ) 
        return email


    def clean_password(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                ) 

            return password1
            

        
