# core/forms.py
from django import forms
from .models import Cliente, Reserva
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Mesa

class UsuarioEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_superuser', 'is_staff', 'is_active']  # Campos que você deseja editar
        labels = {
            'username': 'Nome de Usuário',
            'email': 'Email',
            'is_superuser': 'Status de Superusuário',
            'is_staff': 'Situação da Equipe',
            'is_active': 'Ativo'
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(required=False, label='Membro da Equipe')
    is_superuser = forms.BooleanField(required=False, label='Superusuário')
    is_active = forms.BooleanField(required=True, label='Ativo')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active']

# forms.py

from django import forms
from django.contrib.auth.models import User

class EditUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Nova Senha', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirme a Nova Senha', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', "As senhas não coincidem.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            user.set_password(password1)  # Define a nova senha

        if commit:
            user.save()
        
        return user
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['user', 'telefone',]

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'mesa', 'data_reserva', 'hora_reserva', 'num_pessoas']


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidade']  # Campos da tabela Mesa

