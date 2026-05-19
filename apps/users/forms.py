from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'edad', 'telefono',
                   'genero', 'tipo_documento', 'numero_documento', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['username'].help_text = ''
        self.fields['first_name'].label = 'Nombres'
        self.fields['first_name'].required = True
        self.fields['last_name'].label = 'Apellidos'
        self.fields['last_name'].required = True
        self.fields['edad'].label = 'Edad'
        self.fields['telefono'].label = 'Teléfono'
        self.fields['genero'].label = 'Género'
        self.fields['tipo_documento'].label = 'Tipo de documento'
        self.fields['numero_documento'].label = 'Número de documento'
        self.fields['avatar'].label = 'Foto de perfil'
        self.fields['avatar'].widget.attrs.update({'accept': '.png,.jpg'})

        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'avatar')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})