from rest_framework import serializers
from .models import NetworkNode

class NetworkNodeSerializer(serializers.ModelSerializer):
    level = serializers.ReadOnlyField()

    class Meta:
        model = NetworkNode
        fields = ['id', 'name', 'level', 'debt', 'created_at']