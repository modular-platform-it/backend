# type:ignore
from apps.bot_management.models import TelegramBot, TelegramBotAction, TelegramBotFile
from rest_framework import serializers, validators


class TelegramBotCreateSerializer(serializers.ModelSerializer):
    """Сериализатор телеграм бота при создании и обновлении."""

    name = serializers.CharField(max_length=255)
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
    api_key = serializers.CharField(max_length=255, required=False)
    api_url = serializers.URLField(required=False)

    class Meta:
        model = TelegramBot
        fields = ("id", "name", "telegram_token", "api_key", "api_url")


class TelegramBotShortSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения телеграм бота в списке."""

    name = serializers.CharField(max_length=255)
    telegram_token = serializers.CharField(max_length=255, write_only=True)
    is_started = serializers.BooleanField(read_only=True)
    bot_state = serializers.ChoiceField(TelegramBot.BotState.choices, read_only=True)

    class Meta:
        model = TelegramBot
        fields = ("id", "name", "telegram_token", "is_started", "bot_state")


class TelegramBotSerializer(TelegramBotShortSerializer):
    """Сериализатор для детального отображения телеграм бота."""

    description = serializers.CharField(max_length=1000, required=False)
    api_key = serializers.CharField(max_length=255)
    api_url = serializers.URLField()
    api_availability = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    started_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TelegramBot
        fields = (
            "name",
            "telegram_token",
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
        telegram_bot_pk = self.context["telegram_bot_pk"]
        telegram_bot = TelegramBot.objects.get(id=telegram_bot_pk)
        return telegram_bot.actions.all()


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

    telegram_bot = serializers.PrimaryKeyRelatedField(
        queryset=TelegramBot.objects.all()
    )
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000, required=False)
    command_keyword = serializers.RegexField(r"^/[a-zA-Z0-9_]{1,32}$")
    message = serializers.CharField(max_length=1000, required=False)
    api_key = serializers.CharField(max_length=255, required=False)
    api_url = serializers.URLField(required=False)
    position = serializers.IntegerField(min_value=1, max_value=30)
    is_active = serializers.BooleanField()
    files = TelegramFileSerializer(many=True, required=False)

    def create(self, validated_data):

        action_instance = TelegramBotAction.objects.create(**validated_data)
        if "files" in self.context:
            files = self.context.get("files")
            for file in files:
                TelegramBotFile.objects.create(
                    file=file, telegram_action=action_instance
                )
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
