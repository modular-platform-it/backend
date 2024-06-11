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
    Response403Serializer,
    Response404Serializer,
    ShoppingCartReadSerializer,
    ShoppingCartWriteSerializer,
)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Список карточек товара",
        tags=["Карточки товаров"],
        responses={
            200: openapi.Response("OK", CartSerializer(many=True)),
            404: openapi.Response(
                "Список карточек товара не найден", Response404Serializer()
            ),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Карточки товаров"],
        operation_description="Детальная информация о карточке товара по ее id",
        responses={
            200: openapi.Response("OK", CartSerializer(many=True)),
            400: openapi.Response("Ошибка в поле id", Response400Serializer),
            404: openapi.Response(
                "Карточка товара не найдена", Response404Serializer()
            ),
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Карточки товаров"],
        operation_description="Удаление карточки товара по ее id",
        responses={
            204: openapi.Response("Карточка товара удалена"),
            400: openapi.Response("Ошибка в поле id", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
            404: openapi.Response(
                "Карточка товара не найдена", Response404Serializer()
            ),
        },
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Карточки товаров"],
        operation_description="Изменение всех полей карточки товара по ее id",
        responses={
            200: openapi.Response("Карточка товара обновлена"),
            400: openapi.Response("Ошибка в полях", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
            404: openapi.Response(
                "Карточка товара не найдена", Response404Serializer()
            ),
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Карточки товаров"],
        operation_description="Частичное изменение полей карточки товара по ее id",
        responses={
            200: openapi.Response("Карточка товара обновлена"),
            400: openapi.Response("Ошибка в полях", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
            404: openapi.Response(
                "Карточка товара не найдена", Response404Serializer()
            ),
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Карточки товаров"],
        operation_description="Создание карточки товара",
        responses={
            201: openapi.Response("Карточка товара создана"),
            400: openapi.Response("Ошибка в полях", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
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
        operation_description="Список покупок",
        responses={
            200: openapi.Response("OK", ShoppingCartReadSerializer(many=True)),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
            404: openapi.Response("Список покупок не найден", Response404Serializer()),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Список покупок"],
        operation_description="Детальная информация о списке покупок по id",
        responses={
            200: openapi.Response("OK", ShoppingCartReadSerializer(many=True)),
            400: openapi.Response("Ошибка в поле id", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
            404: openapi.Response("Список покупок не найден", Response404Serializer()),
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Список покупок"],
        operation_description="Удаление списка покупок из корзины по его id",
        responses={
            204: openapi.Response("Список покупок удален"),
            400: openapi.Response("Ошибка в поле id", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
            404: openapi.Response("Список покупок не найден", Response404Serializer()),
        },
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Список покупок"],
        operation_description="Изменение списка покупок по id",
        responses={
            200: openapi.Response("Список покупок обновлен"),
            400: openapi.Response("Ошибка в полях", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
            404: openapi.Response("Список покупок не найден", Response404Serializer()),
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Список покупок"],
        operation_description="Изменение списка покупок по id",
        responses={
            200: openapi.Response("Список покупок обновлен"),
            400: openapi.Response("Ошибка в полях", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
            404: openapi.Response("Список покупок не найден", Response404Serializer()),
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Список покупок"],
        operation_description="Добавление карточки товара по id в список покупок",
        responses={
            201: openapi.Response("Карточка товара добавлена в список покупок"),
            400: openapi.Response("Ошибка в полях", Response400Serializer),
            403: openapi.Response("Требуется авторизация", Response403Serializer),
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
