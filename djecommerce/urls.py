"""djecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store.views import index, product_detail, add_to_cart, cart, cart_delete, contact, add_product, add_category, product_delete, product_edit, order_delete, checkout, my_orders, order_details 
from accounts.views import signup, logout_user, login_user  
from djecommerce import settings 
from django.conf.urls.static import static  


urlpatterns = [
    path('',index, name='index'),
    path('admin/', admin.site.urls),
    #lorsque l'URL est accédée, Django s'attend à ce qu'une chaîne de caractères soit fournie à la place de <str:slug>. Cette chaîne sera ensuite transmise à la vue associée pour être utilisée dans le traitement.
    #slug est utilisé dans l'URL, l'url va nous permettre d'accéder au produit.
    path('product/<str:slug>/', product_detail, name='product'), 
    path('product/<str:slug>/delete', product_delete, name='product_delete'), 
    path('product/<str:slug>/edit', product_edit, name='product_edit'), 
    path('product/<str:slug>/add_to_cart/', add_to_cart, name='add_to_cart'),  
    path('cart/', cart, name='cart'), 
    path('cart/delete', cart_delete, name='cart_delete'), 
    path('cart/order/<int:order_id>/delete/', order_delete, name='order_delete'), 
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('contact/', contact, name='contact'),
    path('add/product', add_product, name='add_product'),
    path('add/category', add_category, name='add_category'),
    path('cart/checkout', checkout, name='checkout'),
    path('my_orders/', my_orders, name='my_orders'),
    # <uuid:order_number> → Permet de capturer l’order_number sous forme d’UUID dans l’URL
    path('my_orders/order_details/<uuid:order_number>/', order_details, name='order_details'),
] +static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT) #Fonction permet de servir les images (fichiers) static à l'intérieur de notre environement de développement 
