from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TransactionViewSet,TransferViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'transfers', TransferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
