from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from .models import NetworkNode, Contact, Product
from .serializers import NetworkNodeSerializer, ContactSerializer, ProductSerializer


class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsActiveEmployee]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact__country']
    permission_classes = [IsActiveEmployee]
