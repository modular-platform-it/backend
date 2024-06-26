import os
from datetime import datetime as dt
from typing import Any, Type

import requests
from django.core.exceptions import ValidationError
from django.db.models import Case, Value, When
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.utils import timezone
from django_filters import rest_framework as df_filters
from djoser import utils
from djoser.conf import settings
from dotenv import load_dotenv
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.drf_spectacular.drf_serializers import (
    DummyActionSerializer,
    DummyBotSerializer,
    DummyFileSerializer,
    DummyHeaderSerializer,
    DummyStartStopBotSerializer,
    DummyTokenErrorSerializer,
    DummyTokenSerializer,
    DummyVariableSerializer,
    ForbiddenSerializer,
    MethodNotAlowedSerializer,
    NotFoundSerializer,
)
from api.exceptions import BotIsRunningException
from api.filters import TelegramBotFilter
from api.serializers import (
    HeaderSerializer,
    TelegramBotActionSerializer,
    TelegramBotCreateActionSerializer,
    TelegramBotCreateSerializer,
    TelegramBotSerializer,
    TelegramBotShortSerializer,
    TelegramFileSerializer,
    TokenSerializer,
    VariableSerializer,
)
from apps.bot_management.models import (
    Header,
    TelegramBot,
    TelegramBotAction,
    TelegramBotFile,
    Variable,
)

load_dotenv()


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404


def check_bot_started(telegram_bot) -> None:
    """
    Проверяет запущен ли бот во время попытки изменения настроек.
    Вызывает ошибку со статусом 400 при положительном результате.
    """
    if isinstance(telegram_bot, int):
        telegram_bot = get_object_or_404(TelegramBot, pk=telegram_bot)

    if isinstance(telegram_bot, TelegramBot) and telegram_bot.is_started:
        raise BotIsRunningException


@extend_schema(tags=["Телеграм боты"])
@extend_schema_view(
    list=extend_schema(
        summary="Список ботов",
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=TelegramBotSerializer),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyBotSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение детальной информации о боте по его id",
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=TelegramBotSerializer),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Телеграм бот не найден"
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удаление бота по его id",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Телеграм бот удален"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyBotSerializer, description="Ошибка в поле id"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Телеграм бот не найден"
            ),
        },
    ),
    update=extend_schema(
        summary="Изменение всех полей бота по его id",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TelegramBotCreateSerializer, description="Бот обновлен"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyBotSerializer,
                description="Ошибка в полях или остановите бота",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Телеграм бот не найден"
            ),
        },
    ),
    create=extend_schema(
        summary="Создание бота",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=TelegramBotCreateSerializer, description="Телеграм бот создан"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyBotSerializer, description="Ошибка в полях"
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное изменение полей бота по его id",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TelegramBotCreateSerializer, description="Бот обновлен"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyBotSerializer,
                description="Ошибка в полях или остановите бота",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Телеграм бот не найден"
            ),
        },
    ),
    check_telegram_token=extend_schema(
        summary="Проверка телеграм_токена",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=DummyTokenSerializer, description="Успех"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyTokenErrorSerializer,
                description="Поле содержит ошибки",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=DummyTokenSerializer, description="Токен не существует"
            ),
            status.HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=MethodNotAlowedSerializer, description="Метод не разрешен."
            ),
        },
    ),
    stop_bot=extend_schema(
        summary="Остановка бота",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=DummyStartStopBotSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyBotSerializer, description="Ошибка в поле id"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(response=NotFoundSerializer),
            status.HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=MethodNotAlowedSerializer, description="Метод не разрешен."
            ),
        },
    ),
    start_bot=extend_schema(
        summary="Запуск бота",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=DummyStartStopBotSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyBotSerializer, description="Ошибка в поле id"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(response=NotFoundSerializer),
            status.HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=MethodNotAlowedSerializer, description="Метод не разрешен."
            ),
        },
    ),
)
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
        "bot_state",
        "created_at",
        "started_at",
    )
    ordering_fields = (
        "name",
        "is_started",
        "bot_state",
        "created_at",
        "started_at",
    )
    ordering = ("bot_state",)
    lookup_field = "pk"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            is_started = {TelegramBot.BotState.RUNNING, TelegramBot.BotState.ERROR}
            return queryset.annotate(
                is_started=Case(
                    When(bot_state__in=is_started, then=Value(True)),
                    default=Value(False),
                )
            )
        return queryset

    def get_serializer_class(
        self,
    ) -> (
        Type[TelegramBotShortSerializer]
        | Type[TelegramBotSerializer | TelegramBotCreateSerializer]
    ):
        match self.action:
            case "list":
                return TelegramBotShortSerializer
            case "retrieve":
                return TelegramBotSerializer
            case "check_telegram_token":
                return TokenSerializer
        return TelegramBotCreateSerializer

    def update(self, request, *args, **kwargs):
        check_bot_started(self.get_object())
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        check_bot_started(self.get_object())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        check_bot_started(self.get_object())
        return super().destroy(request, *args, **kwargs)

    @action(
        methods=["POST"],
        detail=False,
        url_path="check_telegram_token",
        url_name="check_telegram_token",
        serializer_class=TokenSerializer,
    )
    def check_telegram_token(self, request: Request) -> Response:
        """Эндпоинт для проверки введенного телеграм токена на валидность."""
        # TODO переделать в асинхронный вариант
        telegram_token = request.data.get("telegram_token")
        response = requests.get(f"https://api.telegram.org/bot{telegram_token}/getMe")
        if response.ok:
            return Response(data={"detail": True}, status=status.HTTP_200_OK)
        return Response(data={"detail": False}, status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=["GET"],
        detail=True,
        url_name="start_bot",
        permission_classes=(IsAuthenticated,),
    )
    def start_bot(self, request, *args, **kwargs) -> Response:
        BOT_SERVER_URL: str = os.getenv(
            "BOT_SERVER_URL", "http://bot_server:8001/"
        )  # Для докера
        # BOT_SERVER_URL: str = os.getenv("BOT_SERVER_URL", "http://localhost:8001/") # Для локального запуска
        telegram_bot = self.get_object()
        if telegram_bot.is_started:

            return Response(
                data={"detail": "Бот уже запущен"}, status=status.HTTP_200_OK
            )

        response = requests.get(f"{BOT_SERVER_URL}{telegram_bot.pk}/start/")
        if response.status_code != 200:
            return Response(
                {"error": "Не удалось запустить бота"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        telegram_bot.bot_state = TelegramBot.BotState.RUNNING
        telegram_bot.started_at = timezone.now()
        telegram_bot.save()
        return Response(
            data={"detail": "Бот успешно запущен"}, status=status.HTTP_200_OK
        )

    @action(
        methods=["GET"],
        detail=True,
        url_name="stop",
        permission_classes=(IsAuthenticated,),
    )
    def stop_bot(self, request, *args, **kwargs) -> Response:
        BOT_SERVER_URL: str = os.getenv(
            "BOT_SERVER_URL", "http://bot_server:8080/"
        )  # Для докера
        # BOT_SERVER_URL: str = os.getenv("BOT_SERVER_URL", "http://localhost:8001/") # Для локального запуска
        telegram_bot = self.get_object()
        response = requests.get(f"{BOT_SERVER_URL}{telegram_bot.pk}/stop/")

        if telegram_bot.is_started:
            if response.status_code != 200:
                return Response(
                    {"error": "Не удалось остановить бота"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            telegram_bot.bot_state = TelegramBot.BotState.STOPPED
            telegram_bot.save()
            return Response(
                data={"detail": "Бот успешно остановлен"}, status=status.HTTP_200_OK
            )
        return Response(data={"detail": "Бот не запущен"}, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Бот уже остановлен."},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Действия"])
@extend_schema_view(
    list=extend_schema(
        summary="Список действий бота",
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=TelegramBotSerializer),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие не найдено"
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение детальной информации о действии бота по его id",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TelegramBotActionSerializer,
                description="Действие телеграм бота",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyActionSerializer,
                description="Ошибка в полях или остановите бота",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие не найдено"
            ),
        },
    ),
    create=extend_schema(
        summary="Создание действия в боте",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=TelegramBotActionSerializer, description="Действие создано"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyActionSerializer,
                description="Ошибка в полях или остановите бота",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Телеграм бот не найден"
            ),
        },
    ),
    update=extend_schema(
        summary="Изменение всех полей действия бота по его id",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TelegramBotActionSerializer, description="Действие обновлено"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyActionSerializer,
                description="Ошибка в полях или остановите бота",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Телеграм бот не найден"
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное изменение полей действия бота по его id",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TelegramBotActionSerializer, description="Действие обновлено"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyActionSerializer,
                description="Ошибка в полях или остановите бота",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Телеграм бот не найден"
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удаление действия бота по его id",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Действие удалено"),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Телеграм бот не найден"
            ),
        },
    ),
)
class TelegramBotActionViewSet(viewsets.ModelViewSet):
    """Набор представлений для действий телеграм бота."""

    queryset = TelegramBotAction.objects.all()
    serializer_class = TelegramBotActionSerializer
    parser_classes = (FormParser, MultiPartParser)
    lookup_field = "pk"
    permission_classes = (IsAuthenticated,)

    _bot = None

    def get_bot(self):
        if self._bot is None:
            self._bot = get_object_or_404(
                TelegramBot, pk=self.kwargs["telegram_bot_pk"]
            )
        return self._bot

    def get_queryset(self):
        return self.get_bot().actions.all().prefetch_related("files")

    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                return TelegramBotCreateActionSerializer
            case _:
                return self.serializer_class

    def get_serializer_context(self) -> dict[str, Any]:
        context = super(TelegramBotActionViewSet, self).get_serializer_context()
        if len(self.request.FILES) > 0:
            context.update({"files": self.request.FILES.getlist("files")})
        return context

    def update(self, request, *args, **kwargs):
        check_bot_started(self.get_bot())
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        check_bot_started(self.get_bot())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        check_bot_started(self.get_bot())
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(telegram_bot=self.get_bot())

    def create(self, request: Request, *args, **kwargs) -> Response:
        check_bot_started(self.get_bot())
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
        summary="Список файлов",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=TelegramBotSerializer),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение детальной информации о файле по его id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TelegramFileSerializer, description="Файл действия"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyFileSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие или бот не найдены"
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удаление файла по его id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Файл удален"),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие или бот не найдены"
            ),
        },
    ),
    update=extend_schema(
        summary="Изменение всех полей файла по его id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TelegramFileSerializer, description="Файл действия изменен"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyFileSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие или бот не найдены"
            ),
        },
    ),
    create=extend_schema(
        summary="Загрузка файла",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=TelegramFileSerializer, description="Файл действия создан"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyFileSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие или бот не найдены"
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное изменение полей файла по его id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TelegramFileSerializer, description="Файл действия изменен"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyFileSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие или бот не найдены"
            ),
        },
    ),
)
class TelegramBotActionFileViewSet(viewsets.ModelViewSet):
    """Набор представлений для файлов действий телеграм ботов."""

    queryset = TelegramBotFile.objects.all()
    serializer_class = TelegramFileSerializer
    permission_classes = (IsAuthenticated,)

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

    def update(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Пользовательские переменные"])
@extend_schema_view(
    list=extend_schema(
        summary="Список пользовательских переменных",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=TelegramBotSerializer),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение детальной информации о пользовательской переменной по ее id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=VariableSerializer,
                description="Пользовательская переменная действия",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyVariableSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие или бот не найдены"
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удаление пользовательской переменной по ее id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Переменная удалена"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer,
                description="Переменная, действие или бот не найдены",
            ),
        },
    ),
    update=extend_schema(
        summary="Изменение всех полей пользовательской переменной по ее id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=VariableSerializer, description="Переменная действия изменена"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyVariableSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer,
                description="Переменная, действие или бот не найдены",
            ),
        },
    ),
    create=extend_schema(
        summary="Создание пользовательской переменной",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=VariableSerializer, description="Переменная действия создана"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyVariableSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие или бот не найдены"
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное изменение полей пользовательской переменной по ее id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=VariableSerializer, description="Переменная действия изменена"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyVariableSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer,
                description="Переменная, действие или бот не найдены",
            ),
        },
    ),
)
class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Заголовки http запросов"])
@extend_schema_view(
    list=extend_schema(
        summary="Получение списка заголовков",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=TelegramBotSerializer),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение детальной информации о заголовке по его id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=HeaderSerializer,
                description="Пользовательская заголовок http запроса",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyHeaderSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer,
                description="Заголовок, действие или бот не найдены",
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удаление заголовка по его id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Заголовок удален"),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer,
                description="Заголовок, действие или бот не найдены",
            ),
        },
    ),
    update=extend_schema(
        summary="Изменение всех полей заголовка по его id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=VariableSerializer,
                description="Заголовок htttp запроса изменен",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyVariableSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer,
                description="Заголовок, действие или бот не найдены",
            ),
        },
    ),
    create=extend_schema(
        summary="Создание заголовка",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=VariableSerializer, description="Заголовок http запроса создан"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyVariableSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer, description="Действие или бот не найдены"
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное изменение полей заголовка по его id",
        parameters=[
            OpenApiParameter(
                name="telegram_bot_pk", type=int, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=VariableSerializer,
                description="Заголовок http запроса изменен",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DummyVariableSerializer, description="Ошибка в полях"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ForbiddenSerializer, description="Требуется авторизация"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=NotFoundSerializer,
                description="Заголовок, действие или бот не найдены",
            ),
        },
    ),
)
class HeaderViewSet(viewsets.ModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Header.objects.filter(
            telegram_action__telegram_bot=self.kwargs["telegram_bot_pk"],
            telegram_action=self.kwargs["telegram_action_pk"],
        )

    def update(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        check_bot_started(self.kwargs.get("telegram_bot_pk"))
        return super().destroy(request, *args, **kwargs)


class TokenDestroyView(views.APIView):
    """Use this endpoint to logout user (remove user authentication token)."""

    serializer_class = None
    permission_classes = settings.PERMISSIONS.token_destroy

    def post(self, request):
        utils.logout_user(request)
        return Response(
            {"detail": "User logged out successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
