import accounts.views
import django.shortcuts
from django.shortcuts import get_object_or_404
import rest_framework
from store.models import Product, Cart, Order, CartOrder, Category, Size, Color
from django.urls import reverse 
from django.shortcuts import render, redirect 
import django.http
import store.views
from django.contrib import messages
# Importation du décorateur 'login_required' pour restreindre l'accès à la vue aux utilisateurs connectés
import django.contrib.auth.decorators
from django.contrib.auth.decorators import user_passes_test, login_required
from store.forms import AddContactForm, AddProductForm, AddCategoryForm, EditProductForm, BillingAddressForm
from accounts.forms import LoginForm, SignupForm
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.db.models import Sum
import uuid
from django.utils.timezone import now



# La vue nous permet d'accéder à la page d'accueil : 
# Créer un chemin URL qui va etre relié à une vue , cette vue va retourner un fichier html qui est affiché à l'utilisateur.  
def index(request):
    # On crée une instance de chaque formulaire
    login_form = LoginForm()
    signup_form = SignupForm()
    
    categories = Category.objects.all()
    # Récupérer les produits de la base de données 
    products = Product.objects.all()  
    # Appeler render pour transmettre le contexte au modèle (HTML), toutes les clés du dictionnaire contexte sont disponibles dans HTML
    # Dictionnaire = clé products : products "variable" contenant tous les produits de la BDD
    return render(request,'store/index.html', context={"products": products, "categories": categories, 'login_form': login_form, 'signup_form': signup_form }) 


def product_detail(request, slug):
    # Récupérer l'objet Product correspondant au slug passé en paramètre dans l'URL
    product= get_object_or_404(Product, slug=slug) 
    categories = Category.objects.all()
    # Récupérer les produits de la meme catégorie que le produit passé en paramètre (actuel) 
    related_products= Product.objects.filter(category=product.category).exclude(slug=slug)
    # return HttpResponse(f'{product.name} {product.price}£') 
    return render(request, 'store/detail.html',context={'product':product, 'related_products' :  related_products, 'categories':categories, 'login_form':LoginForm(), 'signup_form':SignupForm()}) 

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.delete() 
    messages.success(request, "Le produit a été supprimé avec succès.")
    return redirect ('index') 

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        # request.files pour récupérer l'image téléchargée par le superuser
        edit_product_form = EditProductForm(request.POST, request.FILES, instance=product) 
        if edit_product_form.is_valid():
            # créer une instance product sans l'enregistrer immédiatement dans la base de données. 
            product = edit_product_form.save(commit=False) 
            # enregistrer le produit dans la base de données, seules les données de base (non-ManyToMany) sont enregistrées.
            product.save() 
            # Ajoutez les tailles et les couleurs après avoir sauvegardé le produit; gèrer l'enregistrement des relations ManyToMany
            edit_product_form.save_m2m()
            messages.success(request, f"Votre Article a été modifié")
            # rediriger vers la page du produit nouvellement ajouté.
            return redirect('product', slug = product.slug)  
    else :
        edit_product_form = EditProductForm(instance=product)

    return render(request, 'store/edit_product.html', context={'edit_product_form': edit_product_form, 'product': product, 'login_form':LoginForm(), 'signup_form':SignupForm()}) 

@login_required(login_url='index')
def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)

    # Récupérer la taille, la couleur et la quantité sélectionnées
    size_id = request.POST.get('size')
    color_id = request.POST.get('color')
    quantity = int(request.POST.get('quantity', 1))

    if not size_id or not color_id:
        # Ajoutez un message d'erreur si la taille ou la couleur n'est pas sélectionnée
        messages.error(request, "Veuillez sélectionner une taille et une couleur s'il vous plaît !")
        return redirect(reverse("product", kwargs={"slug": slug}))

    size = get_object_or_404(Size, id=size_id)
    color = get_object_or_404(Color, id=color_id)

    # Vérifier si un panier existe pour l'utilisateur, sinon en créer un
    cart, created_cart = Cart.objects.get_or_create(user=user)
    
    # Vérifier si l'article existe déjà dans le panier avec la même taille et couleur
    order, created_order = Order.objects.get_or_create(user=user, ordered=False, product=product, size=size, color=color)
    
    # Si l'article n'existe pas dans le panier, on le crée
    if created_order:
        order.quantity = quantity  # Fix to set the correct quantity when the order is first created
    else:
        order.quantity += quantity  # Increment by the quantity 
        
    order.save()
        
    # Ajoute la commande au panier si elle n'est pas déja liée
    if order not in cart.orders.all(): 
        cart.orders.add(order)

    # s'auvegarder le panier dans la bdd
    cart.save()
    
    messages.success(request, "Article ajouté au panier avec succès !")
    # Une redirection vers la page du produit
    #return redirect(reverse("product", kwargs={"slug": slug}))
    return redirect('cart') 
    
def cart(request): 
    cart = get_object_or_404(Cart, user= request.user) 
    orders = cart.orders.all()  
    # Calcul du sous-total pour toutes les commandes, subtotal_price est une variable locale. Elle n'est pas une propriété de chaque commande, mais plutôt une valeur calculée qui s'applique à l'ensemble du panier.
    subtotal_price = sum(order.total_price for order in orders)
    total_price_cart = subtotal_price 
    return render(request,'store/cart.html', context={'orders':cart.orders.all(), 'subtotal_price': subtotal_price,
        'total_price_cart': total_price_cart})  


def checkout(request):
    # Récupère le panier de l'utilisateur ou renvoie une erreur 404 si inexistant.
    cart = get_object_or_404(Cart, user= request.user)
    # Récupère toutes les commandes associées à ce panier.
    orders = cart.orders.all()
    # Calcule le prix total des articles dans le panier.
    subtotal_price = sum(order.total_price for order in orders)
    # Définit un coût fixe pour la livraison.
    shipping_cost = 800
    # Calcule le prix total à payer (produits + frais de livraison).
    total_price_cart = subtotal_price + shipping_cost 

    # Traitement du formulaire de facturation si la requête est un POST 
    if request.method == "POST": 
        # Récupère les données du formulaire de facturation.
        billing_address_form = BillingAddressForm(request.POST)
        # Vérifie si le formulaire est valide
        if billing_address_form.is_valid():
            try:
                # Crée l'adresse sans l'enregistrer immédiatement
                billing_address = billing_address_form.save(commit=False)
                # Associer l'utilisateur à l'adresse de facturation
                billing_address.user = request.user 
                billing_address.save()
                print(billing_address.id)
                # Associer l'adresse de facturation au panier
                cart.billing_address = billing_address
                cart.save()

                # Générer un identifiant unique pour ce checkout
                order_number = uuid.uuid4()
                print(order_number)
                # Mise à jour des commandes du panier
                print(orders.count())
                for order in orders:
                    # Associe l'adresse de facturation à la commande.
                    order.billing_address = billing_address
                    # Marque la commande comme passée
                    order.ordered = True
                    order.ordered_date = now().date()
                    order.save()

                    # Créer une instance CartOrder pour chaque Order
                    CartOrder.objects.create(
                        user = request.user,
                        order_number = order_number,
                        cart=cart,
                        order=order,
                        product=order.product,
                        category=order.product.category,
                        billing_address=billing_address,
                        total_price=order.total_price,
                        order_ordered_date=now().date(),  # Mettre aussi la date du jour ici
                     )
                
                # Vider le panier après checkout / validation de la commande 
                cart.orders.clear() # Supprime toutes les commandes du panier (le client a déjà passé sa commande)

                messages.success(request, "Commande passée, veuillez patienter jusqu'à le livreur vous contacte. Merci pour votre confiance !")
                 # Redirige l'utilisateur vers la page précédente ou l'index.
                #return redirect(request.META.get('HTTP_REFERER', 'index'))
                return redirect('my_orders')

            except IntegrityError:
                messages.error(request, "Une erreur est survenue lors de la création de l'adresse de facturation. Veuillez réessayer.")
   
    # Charge un formulaire vide si ce n'est pas une requête POST.
    else:
        billing_address_form = BillingAddressForm()

    # Préparation du contexte pour l'affichage du template checkout.html
    context = {
        'billing_address_form': billing_address_form,
        'orders': orders,
        'subtotal_price': subtotal_price,
        'shipping_cost': shipping_cost,
        'total_price_cart': total_price_cart,
        'login_form': LoginForm(),
        'signup_form': SignupForm()
    }
    
    # Affiche la page de paiement (checkout.html) avec les données envoyées
    return render(request, 'store/checkout.html', context)

# Vue pour afficher les paniers passés : Affiche chaque order_number avec le prix total du panier :
def my_orders(request):
    # Regrouper les commandes par numéro de commande 
    orders_by_number = CartOrder.objects.filter(user=request.user).values(
        'order_number', 'order_ordered_date').annotate(total_price=Sum('total_price'))
    # orders_by_number contient uniquement order_number, total_price et order_ordered_date.
    return render(request, 'store/my_orders.html', {'orders_by_number': orders_by_number})


def order_details(request, order_number):
    # il faut récupérer les commandes qui ont ce order_number :
    orders = CartOrder.objects.filter(user=request.user, order_number= order_number)
    if not orders:
        messages.error(request,'Aucune commande trouvée pour ce panier !')
        return redirect('my_orders')

    return render(request, 'store/order_details.html', {'orders': orders})

def cart_delete(request):
    # Methode 1 : cart = request.user.cart  if cart: 
    if cart:= request.user.cart: 
        cart.delete() #Méthode delete du modèle cart 
    return redirect ('index') 

def order_delete(request, order_id):
    # Récupérer la commande spécifiée par l'identifiant
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    # Rediriger vers la page du panier
    return redirect ('cart') 

def contact(request):
    if  request.method== "POST":
        # valider et traiter les données du formulaire
        contact_form= AddContactForm(request.POST)
        if contact_form.is_valid():
            contact= contact_form.save(commit= False)
            # sauvegarder l'objet Contact dans la base de données et rediriger l'utilisateur vers la page d'accueil
            contact.save()
            messages.success(request,"Message Envoyé !")
            return redirect(request.META.get('HTTP_REFERER', 'index'))
    else:
        contact_form= AddContactForm()

    # afficher le formulaire vide
    return render(request, 'store/contact.html', context= {'contact_form':contact_form, 'login_form':LoginForm(), 'signup_form':SignupForm()})


# restreindre l'accès à la vue add_product aux seuls superutilisateurs. La fonction lambda lambda u: u.is_superuser évalue si l'utilisateur est un superutilisateur ou non.   
@user_passes_test(lambda u: u.is_superuser, login_url='login')
def add_product(request):
    if request.method == 'POST':
        # request.files pour récupérer l'image téléchargée par le superuser
        add_product_form = AddProductForm(request.POST, request.FILES) 
        if add_product_form.is_valid():
            # créer une instance product sans l'enregistrer immédiatement dans la base de données. 
            product = add_product_form.save(commit=False) 
            # enregistrer le produit dans la base de données, seules les données de base (non-ManyToMany) sont enregistrées.
            product.save() 
            # Ajoutez les tailles et les couleurs après avoir sauvegardé le produit; gèrer l'enregistrement des relations ManyToMany
            add_product_form.save_m2m()
            messages.success(request, f"Votre Article a été ajouté")
            # rediriger vers la page du produit nouvellement ajouté.
            return redirect('product', slug = product.slug)  
    else :
        add_product_form = AddProductForm()

    return render(request, 'store/add_product.html', context={'add_product_form': add_product_form, 'login_form':LoginForm(), 'signup_form':SignupForm()})


@user_passes_test(lambda u: u.is_superuser, login_url='login')
def add_category(request):
    if request.method == 'POST':
        add_category_form = AddCategoryForm(request.POST, request.FILES) 
        if add_category_form.is_valid():
            category = add_category_form.save(commit=False)
            category.save()
            messages.success(request, f"Votre Catégorie a été ajoutée")
            return redirect('index')

    else :
        add_category_form = AddCategoryForm()

    return render(request, 'store/add_category.html', context={'add_category_form': add_category_form, 'login_form':LoginForm(), 'signup_form':SignupForm()})


