
from rest_framework.viewsets import ModelViewSet
from purchases.models import Cart, ShoppingCart

from .permissions import IsAdminOrReadOnly, IsAuthenticatednOrReadOnly
from .serializers import CartSerializer, ShoppingCartSerializer


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
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()





