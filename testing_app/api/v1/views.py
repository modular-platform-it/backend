from django.utils.decorators import method_decorator
from djoser.serializers import TokenCreateSerializer
from djoser.views import TokenCreateView, TokenDestroyView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from purchases.models import Cart, ShoppingCart
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAuthenticatedOrReadOnly
from .serializers import (
    CartSerializer,
    Response400Serializer,
    Response401Serializer,
    Response404Serializer,
    ShoppingCartReadSerializer,
    ShoppingCartWriteSerializer,
)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Карточки товаров"],
        responses={
            200: openapi.Response("OK", CartSerializer(many=True)),
            404: openapi.Response("Not Found", Response404Serializer()),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Карточки товаров"],
        responses={
            200: openapi.Response("OK", CartSerializer(many=True)),
            400: openapi.Response("Bad Request", Response400Serializer),
            404: openapi.Response("Not Found", Response404Serializer()),
        },
    ),
)
class CartViewSet(ModelViewSet):
    """Вьюсет карточки товаров"""

    lookup_field = "id"
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Список покупок"],
        responses={
            200: openapi.Response("OK", ShoppingCartReadSerializer(many=True)),
            401: openapi.Response("Unauthorized", Response401Serializer()),
            404: openapi.Response("Not Found", Response404Serializer()),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Список покупок"],
        responses={
            200: openapi.Response("OK", ShoppingCartReadSerializer(many=True)),
            400: openapi.Response("Bad Request", Response400Serializer),
            401: openapi.Response("Unauthorized", Response401Serializer()),
            404: openapi.Response("Not Found", Response404Serializer()),
        },
    ),
)
class ShoppingCartViewSet(ModelViewSet):
    """Вьюсет для списка покупок"""

    lookup_field = "id"
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)
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


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Авторизация"],
        responses={
            204: openapi.Response("No Content"),
            401: openapi.Response("Unauthorized", Response401Serializer()),
        },
    ),
)
class SwaggerLogoutView(TokenDestroyView):
    pass


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Авторизация"],
        responses={
            200: openapi.Response("Ok", TokenCreateSerializer()),
            400: openapi.Response("Bad Request", Response400Serializer),
        },
    ),
)
class SwaggerLoginView(TokenCreateView):
    pass
