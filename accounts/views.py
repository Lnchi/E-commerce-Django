import accounts.views
from django.shortcuts import render, redirect
from django.urls import reverse 
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from accounts.forms import CreateUserForm
from accounts.forms import LoginForm, SignupForm
from django.contrib import messages
from django.http import JsonResponse




#Récupérer le modèle utilisateur en utilisant la fonction get_user_model()
#Le modèle utilisateur que nous utilisons est "Shopper"

         
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        # crée une instance du formulaire vide 
        signup_form = SignupForm() 
        if request.method == 'POST': 
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                # l'objet user est créé en mémoire, mais l'enregistrement réel dans la base de données est retardé. commit=False -> retarder la sauvegarde réelle de l'objet utilisateur  
                user = signup_form.save(commit=False)
                # On récupère le mot de passe
                password = signup_form.cleaned_data["password1"]
                # On définie le mot de passe pour l'utilisateur
                user.set_password(password)
                # Enregistrer le formulaire pour obtenir l'utilisateur créé 
                user.save() 
                # Authentifier l'utilisateur avec les informations fournies 
                user = authenticate(username=user.username, password=password)
                # On connecte l'utilisateur créé au site et le redirigie vers la page d'acceuil 
                login(request, user)
                return JsonResponse({"success":True, "redirect":reverse('index')})

            else :   
                # transformer la structure des erreurs du formulaire en un nouveau dictionnaire où chaque champ est associé à une liste d'erreurs spécifiques à ce champ. 
                errors = {field: [error for error in signup_form.errors[field]] for field in signup_form.errors}
                return JsonResponse({"success":False, "errors": errors })
        # renvoyer l'utilisateur vers la page précédente s'il y a une URL de référence disponible, sinon le rediriger vers la page d'accueil     
        return redirect(request.META.get('HTTP_REFERER', 'index'))


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    login_form = LoginForm()  # L'initialisation du formulaire de connexion (login_form)
    if request.method == 'POST':
        # On récupère les données du formulaire de connexion
        login_form = LoginForm(request.POST)   
        if login_form.is_valid():
            # On extrait le nom d'utilisateur et le mot de passe du formulaire
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # Authentifier l'utilisateur avec les informations fournies
            user = authenticate(username=username, password=password)
            if user:
                # Si les informations sont valides, connecter l'utilisateur
                login(request, user)
                # renvoyer une réponse JSON indiquant que la connexion est réussie et redirigeant éventuellement vers une autre page. 
                # reverse('index') garantit d'utiliser le nom d'URL correctement
                return JsonResponse({"success":True, "redirect":reverse('index')})
                
            else:
                # renvoyer une réponse JSON indiquant que la connexion a échoué et renvoyant des erreurs.
                errors = {"field_errors":"Nom d'utilisateur ou mot de passe incorrect."}
                return JsonResponse({"success":False, "errors": errors})
    # Si la méthode de requête n'est pas POST ou si l'authentification échoue, renvoyer à la page d'index avec les formulaires et les messages.
    return render(request, 'store/index.html', {'login_form': login_form, 'signup_form': SignupForm()})

def logout_user(request):
    logout(request)
    return redirect('index')