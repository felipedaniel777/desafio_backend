from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, TransactionViewSet, UserViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'carteira', WalletViewSet, basename='carteira')
router.register(r'transacoes', TransactionViewSet, basename='transacoes')

urlpatterns = [
    path('', include(router.urls)),
]
