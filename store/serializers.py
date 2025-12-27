from rest_framework import serializers
from .models import Category, Product

#we need a serialized representation:transformed and simplified version of complex data (converted to JSON), suitable for transport over an API
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'