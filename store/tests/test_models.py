from django.contrib.auth import get_user_model
import uuid
from store.models import CartOrder, Order, Product, Category, Cart, BillingAddress, Size, Color
from datetime import date


# Vérifier que le modèle CartOrder fonctionne comme prévu
User=get_user_model()

Class CartOrderModelTest(TestCase):
def setUp(self):
    # Créer un utilisateur
    self.user = User.Objects.create_user(username='testuser', password='pass')

