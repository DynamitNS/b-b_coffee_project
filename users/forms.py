from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


User = get_user_model()


class SiteAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Логин', 'class': 'form-input'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-input'}),
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-input'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля', 'class': 'form-input'}),
        }
