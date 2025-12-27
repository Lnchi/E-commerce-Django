from django.db import models
from django.urls import reverse 
from django.utils import timezone
from djecommerce.settings import AUTH_USER_MODEL
import uuid 


class Category (models.Model):

    name=models.CharField(max_length=128)
    thumbnail= models.ImageField(upload_to="categories",blank=True,null=True)

    class Meta:
            verbose_name_plural = "Categories"
            ordering=("name",) # categories classées par leurs nom(name)

    def __str__(self):
        return f"{self.name}"

class Size (models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"


class Color(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

#Cette classe va hériter de models.model, qui est la classe de base pour tous les modèles.
#La variable "product" est une instance de la classe Product.
class Product(models.Model):
 # crée un moyen d'accéder aux objets liés (products) à partir de l'objet source (category) avec related_name='products'.
 category= models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True) # on_delete=models.CASCADE ---> Si on choisi de supprimer une catégorie, les produites reliés à cette catégorie sont également supprimées
 name= models.CharField(max_length=128)
 slug= models.SlugField(max_length=128) 
 price= models.FloatField(default=0.0) 
 stock= models.IntegerField(default=0)
 description= models.TextField(blank=True)
 sizes = models.ManyToManyField(Size, related_name='products')
 colors = models.ManyToManyField(Color, related_name='products')
 thumbnail= models.ImageField(upload_to="products", blank=True,null=True) #upload_to="products" si on veut que les images téléchargées via ce champ seront stockées dans le dossier "media/products/" 
 out_of_stock = models.BooleanField(default=False)  # represent stock status

#Méthode utilisée pour représenter notre instance sous forme de chaîne de caractères. Dans ce cas, nous allons retourner le nom du produit qui sera affiché dans l'interface d'administration.  
 def __str__(self):
    return f"{self.name}({self.stock})"     
#Le nom de l'URL est défini comme 'product' dans l'attribut name 
 def get_absolute_url(self):
    return reverse("product", kwargs={"slug": self.slug}) #Le self.slug de l'instance du produit,il est passé au paramètre "slug" de notre URL.

class BillingAddress(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    region = models.CharField(max_length=100) 
    municipality = models.CharField(max_length=100) 
    street = models.CharField(max_length=100) 
    postal_code = models.CharField(max_length=15) 

#Commande (order)
class Order (models.Model):
 #ForeignKey : Relation plusieurs à un (plusieurs articles reliés à un utilisateur)
 user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)
 username = models.CharField(max_length=30, default="Default Color")
 product = models.ForeignKey(Product, on_delete = models.CASCADE)
 product_name = models.CharField(max_length=128, default="Default Product")
 product_price= models.FloatField(default=0.0) 
 quantity = models.IntegerField(default=1)
 size = models.ForeignKey(Size, on_delete=models.CASCADE)
 size_name = models.CharField(max_length=10,default="XS")
 color = models.ForeignKey(Color, on_delete=models.CASCADE)
 color_name = models.CharField(max_length=20, default="Default Color")
 ordered_date = models.DateField(blank=True, null=True)
 #ordered : Si l'article a été passé / commandé ou pas
 ordered = models.BooleanField(default=False) 
 billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null=True, blank=True)

 #Méthode save surchargée : pour garantir que ces champs sont toujours mis à jour avec les valeurs actuelles avant la sauvegarde.
 def save(self, *args, **kwargs):
    self.username = self.user.username
    self.product_name = self.product.name
    self.product_price = self.product.price
    self.size_name = self.size.name
    self.color_name = self.color.name
    super(Order, self).save(*args, **kwargs)
# chaque instance de Order enregistrera automatiquement le nom d'utilisateur et le nom du produit au moment de la création de la commande. Cela fournira une traçabilité accrue des détails de chaque commande.
 
 def __str__(self):
      return f"{self.product.name}" 
# Méthode pour calculer dynamiquement le prix total pour chaque commande en utilisant un décorateur pour permettre de définir une méthode qui peut être accédée comme une attribut d'instance
# total_price est une propriété de l'objet order , calculée individuellement pour chaque commande dans le panier. Utilisée pour stocker des valeurs spécifiques à chaque instance d'objet.
 @property
 def total_price(self):
      return self.product.price * self.quantity

# CartOrder (Commande de Panier) :
# Relier un Cart à un Order avec des détails spécifiques sur chaque commande.
class CartOrder(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)
    username = models.CharField(max_length=30)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    # ForeignKey : un même order_number doit être partagé entre plusieurs CartOrder 
    # OneToOneField : une seule correspondance entre CartOrder et Order (1 CartOrder = 1 Order).
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    # Ajouter un identifiant pour chaque checkout et permettra de regrouper les commandes du même panier.
    # unique=False pour utiliser le même order_number pour plusieurs commandes dans un même panier.
    order_number = models.UUIDField(default=uuid.uuid4, editable=False)
    order_quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    category_name = models.CharField(max_length=128)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    product_name = models.CharField(max_length=128)
    product_price= models.FloatField(default=0.0) 
    size_name = models.CharField(max_length=10)
    color_name = models.CharField(max_length=20)
    order_ordered_date = models.DateField(blank=True, null=True)
    order_ordered = models.BooleanField(default=False) 
    total_price = models.FloatField()
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    billing_address_first_name = models.CharField(max_length=100)
    billing_address_last_name = models.CharField(max_length=100)
    billing_address_email = models.EmailField()
    billing_address_mobile_no = models.CharField(max_length=15)
    billing_address_region = models.CharField(max_length=100) 
    billing_address_municipality = models.CharField(max_length=100) 
    billing_address_street = models.CharField(max_length=100) 
    

    def save(self, *args, **kwargs):
        self.username = self.user.username
        self.order_quantity = self.order.quantity
        self.category_name = self.category.name
        self.product_name = self.product.name
        self.product_price = self.product.price
        self.size_name = self.order.size.name
        self.color_name = self.order.color.name
        self.order_ordered_date = self.order.ordered_date
        self.order_ordered = self.order.ordered
        self.total_price = self.order.total_price
        if self.billing_address:
            self.billing_address_first_name = self.billing_address.first_name
            self.billing_address_last_name = self.billing_address.last_name
            self.billing_address_email = self.billing_address.email
            self.billing_address_mobile_no = self.billing_address.mobile_no
            self.billing_address_region = self.billing_address.region
            self.billing_address_municipality = self.billing_address.municipality
            self.billing_address_street = self.billing_address.street
        super(CartOrder, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.user.username 

#Panier (cart)
class Cart (models.Model):
 #Un seul panier relié à un seul utilisateur spécifique
 user = models.OneToOneField(AUTH_USER_MODEL, on_delete = models.CASCADE) 
 #Un panier peut contenir plusieurs commandes (instances de CartOrder)
 orders = models.ManyToManyField('Order', related_name='carts')
 billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null=True, blank=True)
 payment_status = models.CharField(max_length=50, default='Pending')

 
 def __str__(self):
     return self.user.username 
 
 #La méthode 'delete' peut être surchargée pour permettre son parcours lors de la suppression d'un panier, 
 #que ce soit par le biais de l'interface d'administration ou toute autre méthode.
 def delete (self, *args, **kwargs):
     for order in self.orders.all():
        order.ordered = True
        order.ordered_date = timezone.now()
        order.save() 
     #clear() : Détacher les articles du panier 
     self.orders.clear() 
     super().delete(*args, **kwargs) 



class Contact(models.Model):
    name= models.CharField(max_length=128)
    email= models.EmailField(max_length=128)
    subject= models.CharField(max_length=128)
    message= models.TextField(blank=False)

    def __str__(self):
        return self.name



    