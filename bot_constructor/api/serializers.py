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
            "bot_state",
            "api_key",
            "api_url",
            "api_availability",
            "is_started",
            "created_at",
            "started_at",
        )


class TelegramFileSerializer(serializers.ModelSerializer):
    """Сериализатор файлов для команд телеграм бота."""

    file = serializers.FileField()

    class Meta:
        model = TelegramBotFile
        fields = (
            "id",
            "file",
        )


class TelegramBotActionSerializer(serializers.ModelSerializer):
    """Сериализатор команд телеграм бота."""

    telegram_bot = serializers.PrimaryKeyRelatedField(
        queryset=TelegramBot.objects.all()
    )
    name = serializers.CharField(max_length=255)
    command_keyword = serializers.RegexField(r"^/[a-zA-Z0-9_]{1,32}$")
    message = serializers.CharField(max_length=1000, required=False)
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
            "command_keyword",
            "message",
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
