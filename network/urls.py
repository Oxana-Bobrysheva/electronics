from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, ContactViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'network-nodes', NetworkNodeViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
