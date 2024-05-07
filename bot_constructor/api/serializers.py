# type:ignore
from typing import IO, Any

from rest_framework import serializers, validators

from apps.bot_management import constants
from apps.bot_management.models import TelegramBot, TelegramBotAction, TelegramBotFile


class TelegramBotCreateSerializer(serializers.ModelSerializer):
    """Сериализатор телеграм бота при создании и обновлении."""

    name = serializers.RegexField(
        regex=rf"^[a-zA-Zа-яёА-ЯЁ]{{{constants.MIN_LETTERS}}}[\w\W]"
        rf"{{{0},{constants.BOT_NAME_LENGTH - constants.MIN_LETTERS - 1}}}\S$"
    )
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

    class Meta:
        model = TelegramBot
        fields = ("id", "name", "telegram_token", "description", "api_key", "api_url")


class TelegramBotShortSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения телеграм бота в списке."""

    name = serializers.RegexField(
        regex=rf"^[a-zA-Zа-яёА-ЯЁ]{{{constants.MIN_LETTERS}}}[\w\W]"
        rf"{{{0},{constants.BOT_NAME_LENGTH - constants.MIN_LETTERS - 1}}}\S$"
    )
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
        telegram_bot_pk = view.kwargs.get("telegram_bot_pk")
        telegram_bot = TelegramBot.objects.get(id=telegram_bot_pk)
        if view.kwargs.get("pk"):
            return telegram_bot.actions.exclude(pk=view.kwargs.get("pk")).all()
        return telegram_bot.actions.all()


class TelegramBotPKField(serializers.PrimaryKeyRelatedField):
    """
    Поле сериализатора для телеграм бота.
    выводит только бота, к которому принадлежит действие.
    """

    def get_queryset(self) -> TelegramBot:
        view = self.context.get("view")
        telegram_bot_pk = view.kwargs.get("telegram_bot_pk")
        return TelegramBot.objects.filter(id=telegram_bot_pk)


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


class TelegramBotActionSerializer(serializers.ModelSerializer):
    """Сериализатор команд телеграм бота."""

    telegram_bot = TelegramBotPKField()
    name = serializers.RegexField(
        regex=rf"^[a-zA-Zа-яёА-ЯЁ]{{{constants.MIN_LETTERS}}}[\w\W]"
        rf"{{{0},{constants.ACTION_NAME_LENGTH - constants.MIN_LETTERS - 1}}}\S$"
    )
    command_keyword = serializers.RegexField(regex=r"^/[a-zA-Z0-9_]{1,32}$")
    position = serializers.IntegerField(min_value=1, max_value=constants.MAX_POSITIONS)
    files = TelegramFileSerializer(many=True, required=False)
    next_action = TelegramBotActionsPKField(required=False)

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
            "description",
            "command_keyword",
            "message",
            "api_key",
            "api_url",
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

    telegram_token = serializers.RegexField(regex=r"^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$")

    class Meta:
        fields = ("telegram_token",)
