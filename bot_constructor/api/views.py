# type:ignore
from api.filters import TelegramBotFilter
from api.serializers import (
    TelegramBotActionSerializer,
    TelegramBotCreateSerializer,
    TelegramBotSerializer,
    TelegramBotShortSerializer,
    TelegramFileSerializer,
)
from apps.bot_management.models import TelegramBot, TelegramBotAction, TelegramBotFile
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as df_filters
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response


class TelegramBotViewSet(viewsets.ModelViewSet):
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

    def get_serializer_class(self):
        if self.action == "list":
            return TelegramBotShortSerializer
        if self.action == "retrieve":
            return TelegramBotSerializer
        return TelegramBotCreateSerializer


class TelegramBotActionViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramBotActionSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        return TelegramBotAction.objects.filter(
            telegram_bot=self.kwargs["telegram_bot_pk"]
        ).prefetch_related("files")

    def list(self, request: Request, telegram_bot_pk: int):
        queryset = TelegramBotAction.objects.filter(telegram_bot=telegram_bot_pk)
        serializer = TelegramBotActionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int, telegram_bot_pk: int):
        queryset = TelegramBotAction.objects.filter(pk=pk, telegram_bot=telegram_bot_pk)
        telegram_action = get_object_or_404(queryset, pk=pk)
        serializer = TelegramBotActionSerializer(telegram_action)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(TelegramBotActionViewSet, self).get_serializer_context()
        if len(self.request.FILES) > 0:
            context.update({"files": self.request.FILES.getlist("files")})
        return context

    def create(self, request: Request, *args, **kwargs):
        file_serializer = TelegramFileSerializer(data=request.FILES, many=True)
        file_serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TelegramBotActionFileViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramFileSerializer

    def get_queryset(self):
        return TelegramBotFile.objects.filter(
            telegram_action__telegram_bot=self.kwargs["telegram_bot_pk"],
            telegram_action=self.kwargs["telegram_action_pk"],
        )

    def list(self, request, telegram_bot_pk: int, telegram_action_pk: int):
        queryset = TelegramBotFile.objects.filter(
            telegram_action__telegram_bot=telegram_bot_pk,
            telegram_action=telegram_action_pk,
        )
        serializer = TelegramFileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, telegram_bot_pk, telegram_action_pk):
        queryset = TelegramBotFile.objects.filter(
            pk=pk,
            telegram_action=telegram_action_pk,
            telegram_action__telegram_bot=telegram_bot_pk,
        )
        file = get_object_or_404(queryset, pk=pk)
        serializer = TelegramFileSerializer(file)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        print(args)
        print(kwargs)
        return super().create(request, *args, **kwargs)
