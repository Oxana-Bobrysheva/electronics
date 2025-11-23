from rest_framework import serializers
from .models import NetworkNode, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'country', 'city', 'street', 'house_number']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'model', 'release_date']


class NetworkNodeSerializer(serializers.ModelSerializer):
    level = serializers.ReadOnlyField()
    contact = ContactSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = NetworkNode
        fields = ['id', 'name', 'level', 'debt', 'created_at', 'contact',
                  'products', 'supplier_name']
        read_only_fields = ['debt']
