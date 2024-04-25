
from rest_framework.viewsets import ModelViewSet
from purchases.models import Cart, ShoppingCart

from .permissions import IsAdminOrReadOnly, IsAuthenticatednOrReadOnly
from .serializers import CartSerializer, ShoppingCartReadSerializer, ShoppingCartWriteSerializer


class CartViewSet(ModelViewSet):
    lookup_field = "id"
    pagination_class = None
    permission_classes = (IsAuthenticatednOrReadOnly,)
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

class ShoppingCartViewSet(ModelViewSet):
    lookup_field = "id"
    pagination_class = None
    permission_classes = (IsAuthenticatednOrReadOnly,)
    queryset = ShoppingCart.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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





