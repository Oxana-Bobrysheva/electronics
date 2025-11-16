from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import NetworkNode
from .serializers import NetworkNodeSerializer

class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact__country']