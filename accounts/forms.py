import django.contrib.auth
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    #  le formulaire doit inclure le champ "password" pour l'authentification.
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control border-0 py-4', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control border-0 py-4', 'placeholder': 'Password'}))


# SignupForm défini comme une sous-classe de UserCreationForm, une classe fournie par Django pour la création d'utilisateurs
# le champ de mot de passe est déjà pris en charge par la classe elle-même.
class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control border-0 py-4', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control border-0 py-4', 'placeholder': 'Confirm Password'}))
    # class Meta fournie des métadonnées supplémentaires sur la façon dont le formulaire doit fonctionner.
    # spécifier le modèle associé au formulaire et les champs à inclure dans le formulaire.
    class Meta:
        # récupérer le modèle utilisateur configuré dans les paramètres Django
        model = get_user_model()
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control border-0 py-4', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-0 py-4', 'placeholder': 'Email'}),
        }


