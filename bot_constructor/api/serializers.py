from typing import IO, Any

from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from rest_framework import serializers, validators

from apps.bot_management import constants, regexps
from apps.bot_management.models import (
    Header,
    TelegramBot,
    TelegramBotAction,
    TelegramBotFile,
    Variable,
)

User = get_user_model()


class DefaultChoiceField(serializers.ChoiceField):

    def __init__(self, default, **kwargs):
        kwargs["default"] = default
        kwargs["allow_blank"] = True
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data == "":
            data = self.default
        return super().to_internal_value(data)


class RequiredBooleanFiled(serializers.BooleanField):
    default_empty_html = serializers.empty


class CurrentBot:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context.get("view").get_bot()

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class TelegramBotCreateSerializer(serializers.ModelSerializer):
    """Сериализатор телеграм бота при создании и обновлении."""

    telegram_token = serializers.RegexField(
        regex=r"^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$",
        validators=(
            validators.UniqueValidator(
                TelegramBot.objects.all(),
                message="Такой токен уже используется",
            ),
        ),
        write_only=True,
    )

    name = serializers.CharField(
        validators=(
            validators.UniqueValidator(
                TelegramBot.objects.all(),
                message="Такое имя уже используется",
                lookup="iexact",
            ),
        ),
    )

    class Meta:
        model = TelegramBot
        fields = ("id", "name", "telegram_token", "description", "api_key", "api_url")


class TelegramBotShortSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения телеграм бота в списке."""

    is_started = serializers.BooleanField(read_only=True)

    class Meta:
        model = TelegramBot
        fields = ("id", "name", "description", "is_started", "bot_state")


class TelegramBotSerializer(TelegramBotShortSerializer):
    """Сериализатор для детального отображения телеграм бота."""

    class Meta:
        model = TelegramBot
        fields = (
            "name",
            "description",
            "bot_state",
            "api_key",
            "api_url",
            "api_availability",
            "is_started",
            "created_at",
            "started_at",
        )


class TelegramBotActionsPKField(serializers.PrimaryKeyRelatedField):
    """
    Поле сериализатора для действий телеграм бота.
    выводит только действия, принадлежащие конкретному боту.
    """

    def get_queryset(self):
        view = self.context.get("view")
        queryset = view.get_queryset()
        if view.kwargs.get("pk"):
            return queryset.exclude(pk=view.kwargs.get("pk")).all()
        return queryset.all()


class TelegramActionVariablesPKField(serializers.PrimaryKeyRelatedField):
    """
    Поле сериализатора для переменных действий телеграм бота.
    выводит только переменные, принадлежащие конкретному действию.
    """

    def get_queryset(self):
        view = self.context.get("view")
        telegram_action_pk = view.kwargs.get("telegram_action_pk")
        telegram_action = TelegramBotAction.objects.get(id=telegram_action_pk)
        return telegram_action.variables.all()


class TelegramFileSerializer(serializers.ModelSerializer):
    """Сериализатор файлов для команд телеграм бота."""

    telegram_action = TelegramBotActionsPKField()
    file = serializers.FileField()

    class Meta:
        model = TelegramBotFile
        fields = (
            "id",
            "telegram_action",
            "file",
        )


class VariableSerializer(serializers.ModelSerializer):
    """Сериализатор для пользовательской переменной."""

    telegram_action = TelegramBotActionsPKField()
    name = serializers.RegexField(regex=regexps.VARIABLE_REGEXP)

    class Meta:
        model = Variable
        fields = ("id", "telegram_action", "name")


class HeaderSerializer(serializers.ModelSerializer):
    """Сериализатор для заголовка пользовательского http запроса."""

    name = serializers.RegexField(regex=regexps.HEADER_REGEXP)

    class Meta:
        model = Header
        fields = ("id", "telegram_action", "name")


class TelegramBotActionSerializer(serializers.ModelSerializer):
    """Сериализатор отображения команд телеграм бота."""

    class Meta:
        model = TelegramBotAction
        fields = (
            "id",
            "telegram_bot",
            "name",
            "action_type",
            "description",
            "command_keyword",
            "message",
            "api_key",
            "api_url",
            "api_method",
            "data",
            "files",
            "position",
            "next_action",
            "is_active",
        )


class TelegramBotCreateActionSerializer(serializers.ModelSerializer):
    """Сериализатор команд телеграм бота."""

    telegram_bot = serializers.HiddenField(default=CurrentBot())
    command_keyword = serializers.RegexField(regex=regexps.COMMAND_KEYWORD_REGEXP)
    position = serializers.IntegerField(min_value=1, max_value=constants.MAX_POSITIONS)
    files = TelegramFileSerializer(many=True, required=False)
    next_action = TelegramBotActionsPKField(required=False, allow_null=True)
    data = serializers.JSONField(required=False)
    is_active = RequiredBooleanFiled(required=True)
    action_type = DefaultChoiceField(
        choices=TelegramBotAction.ActionType,
        default=TelegramBotAction.ActionType.Handlers,
    )

    def create(self, validated_data: dict[str, Any]):
        """
        Дополнительно модифицированый стандартный метод create().
        Добавлена возможность обработки сразу нескольких файлов одним пакетом.

        """
        action_instance = TelegramBotAction.objects.create(**validated_data)
        if "files" in self.context:
            files: list[IO] = self.context.get("files")
            telegram_files: list = []
            for file in files:
                telegram_files.append(
                    TelegramBotFile(file=file, telegram_action=action_instance)
                )
            TelegramBotFile.objects.bulk_create(telegram_files)
        return action_instance

    class Meta:
        model = TelegramBotAction
        fields = (
            "id",
            "telegram_bot",
            "name",
            "action_type",
            "description",
            "command_keyword",
            "message",
            "api_key",
            "api_url",
            "api_method",
            "data",
            "files",
            "position",
            "next_action",
            "is_active",
        )
        validators = (
            validators.UniqueTogetherValidator(
                queryset=TelegramBotAction.objects.all(),
                fields=("telegram_bot", "position"),
            ),
        )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для телеграм токена."""

    telegram_token = serializers.RegexField(
        regex=regexps.TELEGRAM_TOKEN_REGEXP, write_only=True
    )

    class Meta:
        fields = ("telegram_token",)


class TelegramBotActionBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для действий телеграм бота."""

    telegram_bot = serializers.PrimaryKeyRelatedField(read_only=True)
    position = serializers.IntegerField(min_value=1, max_value=constants.MAX_POSITIONS)
    next_action = TelegramBotActionsPKField(required=False)

    class Meta:
        model = TelegramBotAction
        fields = (
            "id",
            "telegram_bot",
            "name",
            "description",
            "position",
            "next_action",
            "is_active",
        )
        validators = (
            validators.UniqueTogetherValidator(
                queryset=TelegramBotAction.objects.all(),
                fields=("telegram_bot", "position"),
            ),
        )


class TelegramBotActionHttpRequestSerializer(TelegramBotActionBaseSerializer):
    """Сериализатор действия API запроса к списку."""

    api_url = serializers.URLField(required=True)
    api_method = serializers.ChoiceField(
        choices=TelegramBotAction.APIMethodType.choices, required=True
    )
    headers = HeaderSerializer(many=True, required=False)
    variables = VariableSerializer(many=True, required=False)

    class Meta:
        model = TelegramBotAction
        fields = (
            "id",
            "telegram_bot",
            "name",
            "action_type",
            "description",
            "command_keyword",
            "api_url",
            "api_key",
            "api_method",
            "headers",
            "variables",
            "data",
            "position",
            "next_action",
            "is_active",
        )


class TelegramBotActionMessageSerializer(TelegramBotActionBaseSerializer):
    """Сериализатор действий отправки сообщения или запроса."""

    files = TelegramFileSerializer(many=True, required=False)

    class Meta:
        model = TelegramBotAction
        fields = (
            "id",
            "telegram_bot",
            "name",
            "action_type",
            "description",
            "command_keyword",
            "message",
            "files",
            "position",
            "next_action",
            "is_active",
        )

    def create(self, validated_data: dict[str, Any]):
        """
        Дополнительно модифицированый стандартный метод create().
        Добавлена возможность обработки сразу нескольких файлов одним пакетом.

        """

        action_instance = TelegramBotAction.objects.create(**validated_data)
        if "files" in self.context:
            files: list[IO] = self.context.get("files")
            telegram_files: list = []
            for file in files:
                telegram_files.append(
                    TelegramBotFile(file=file, telegram_action=action_instance)
                )
            TelegramBotFile.objects.bulk_create(telegram_files)
        return action_instance


class CustomTokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")
    email = serializers.SerializerMethodField()

    class Meta:
        model = settings.TOKEN_MODEL
        fields = ("auth_token", "email")

    def get_email(self, obj) -> str:
        return obj.user.email
