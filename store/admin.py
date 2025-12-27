from django.contrib import admin
from store.models import Product, Order, Cart  
from store.models import Category
# Register your models here. -> Pour l'afficher dans l'interface de l'administration  

admin.site.register(Product) 
admin.site.register(Order) 
admin.site.register(Cart) 
admin.site.register(Category)