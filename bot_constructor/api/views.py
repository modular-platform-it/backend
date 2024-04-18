# type:ignore
from typing import Any

import requests
from api.filters import TelegramBotFilter
from api.serializers import (
    TelegramBotActionSerializer,
    TelegramBotCreateSerializer,
    TelegramBotSerializer,
    TelegramBotShortSerializer,
    TelegramFileSerializer,
    TokenSerializer,
)
from apps.bot_management.models import TelegramBot, TelegramBotAction, TelegramBotFile
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as df_filters
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response


@extend_schema(tags=["Телеграм боты"])
class TelegramBotViewSet(viewsets.ModelViewSet):
    """Набор представлений для телеграм ботов."""

    queryset = TelegramBot.objects.all()
    filter_backends = (
        df_filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = TelegramBotFilter
    search_fields = (
        "^name",
        "is_started",
        "bot_status",
        "created_at",
        "started_at",
    )
    ordering_fields = (
        "name",
        "is_started",
        "bot_status",
        "created_at",
        "started_at",
    )
    ordering = ("-created_at",)
    lookup_field = "pk"

    def get_serializer_class(
        self,
    ) -> type(TelegramBotShortSerializer) | type(
        TelegramBotSerializer | type(TelegramBotCreateSerializer)
    ):
        if self.action == "list":
            return TelegramBotShortSerializer
        if self.action == "retrieve":
            return TelegramBotSerializer
        if self.action == "check_telegram_token":
            return TokenSerializer
        return TelegramBotCreateSerializer

    @action(
        methods=["POST"],
        detail=False,
        url_path="check_telegram_token",
        url_name="check_telegram_token",
        serializer_class=TokenSerializer,
    )
    def check_telegram_token(self, request: Request) -> Response:
        """Эндпоинт для проверки введенного телеграм токена на валидность."""
        telegram_token = request.data.get("telegram_token")
        response = requests.get(f"https://api.telegram.org/bot{telegram_token}/getMe")
        if response.ok:
            return Response(
                data={"detail": "Проверка пройдена успешно"}, status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "Данный токен не действителен"}, status=status.HTTP_404_NOT_FOUND
        )


@extend_schema(tags=["Действия"])
class TelegramBotActionViewSet(viewsets.ModelViewSet):
    """Набор представлений для действий телеграм бота."""

    queryset = TelegramBotAction.objects.all()
    serializer_class = TelegramBotActionSerializer
    parser_classes = (FormParser, MultiPartParser)
    lookup_field = "pk"

    def get_queryset(self):
        return TelegramBotAction.objects.filter(
            telegram_bot=self.kwargs["telegram_bot_pk"]
        ).prefetch_related("files")

    def list(self, request: Request, telegram_bot_pk: int) -> Response:
        queryset = TelegramBotAction.objects.filter(telegram_bot_id=telegram_bot_pk)
        serializer = TelegramBotActionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int, telegram_bot_pk: int) -> Response:
        queryset = TelegramBotAction.objects.filter(pk=pk, telegram_bot=telegram_bot_pk)
        telegram_action = get_object_or_404(queryset, pk=pk)
        serializer = TelegramBotActionSerializer(telegram_action)
        return Response(serializer.data)

    def get_serializer_context(self) -> dict[str, Any]:
        context = super(TelegramBotActionViewSet, self).get_serializer_context()
        if len(self.request.FILES) > 0:
            context.update({"files": self.request.FILES.getlist("files")})
        return context

    def create(self, request: Request, *args, **kwargs) -> Response:
        file_serializer = TelegramFileSerializer(data=request.FILES, many=True)
        file_serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


@extend_schema(tags=["Файлы"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ]
    ),
    destroy=extend_schema(
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ]
    ),
    update=extend_schema(
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ]
    ),
    create=extend_schema(
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ]
    ),
    partial_update=extend_schema(
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ]
    ),
)
class TelegramBotActionFileViewSet(viewsets.ModelViewSet):
    """Набор представлений для файлов действий телеграм ботов."""

    queryset = TelegramBotFile.objects.all()
    serializer_class = TelegramFileSerializer

    def get_queryset(self):
        return TelegramBotFile.objects.filter(
            telegram_action__telegram_bot=self.kwargs["telegram_bot_pk"],
            telegram_action=self.kwargs["telegram_action_pk"],
        )

    def get_serializer_context(self) -> dict[str, Any]:
        context: dict[str, Any] = super(
            TelegramBotActionFileViewSet, self
        ).get_serializer_context()
        context.update({"telegram_bot_pk": self.kwargs["telegram_bot_pk"]})
        return context

    def list(
        self, request: Request, telegram_bot_pk: int, telegram_action_pk: int
    ) -> Response:
        queryset = TelegramBotFile.objects.filter(
            telegram_action__telegram_bot=telegram_bot_pk,
            telegram_action=telegram_action_pk,
        )
        serializer = TelegramFileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(
        self, request, pk: int, telegram_bot_pk: int, telegram_action_pk: int
    ) -> Response:
        queryset = TelegramBotFile.objects.filter(
            pk=pk,
            telegram_action=telegram_action_pk,
            telegram_action__telegram_bot=telegram_bot_pk,
        )
        file: TelegramBotFile = get_object_or_404(queryset, pk=pk)
        serializer: TelegramFileSerializer = TelegramFileSerializer(file)
        return Response(serializer.data)
