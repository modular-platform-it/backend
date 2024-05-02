from purchases.models import Cart, ShoppingCart
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrReadOnly, IsAuthenticatednOrReadOnly
from .serializers import (
    CartSerializer,
    ShoppingCartReadSerializer,
    ShoppingCartWriteSerializer,
)


class CartViewSet(ModelViewSet):
    """Вьюсет карточки товаров"""

    lookup_field = "id"
    pagination_class = None
    permission_classes = (IsAuthenticatednOrReadOnly,)
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class ShoppingCartViewSet(ModelViewSet):
    """Вьюсет для списка покупок"""

    lookup_field = "id"
    pagination_class = None
    permission_classes = (IsAuthenticatednOrReadOnly,)
    queryset = ShoppingCart.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ShoppingCart.objects.filter(user=user)
        else:
            queryset = ShoppingCart.objects.filter(user=1)
        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ShoppingCartReadSerializer
        return ShoppingCartWriteSerializer
