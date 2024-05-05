# type:ignore
from apps.bot_management import constants
from django.core import validators
from django.db import models


class TelegramBot(models.Model):
    """Модель телеграм бота."""

    class BotState(models.TextChoices):
        DRAFT = "DRAFT", "Черновик"
        RUNNING = "RUNNING", "Запущен"
        STOPPED = "STOPPED", "Остановлен"
        ERROR = "ERROR", "Ошибка"

    name = models.CharField(
        verbose_name="Название бота",
        max_length=constants.BOT_NAME_LENGTH,
    )
    telegram_token = models.CharField(
        verbose_name="Токен авторизации телеграм бота",
        max_length=constants.TELEGRAM_TOKEN_LENGTH,
        unique=True,
        validators=(
            validators.RegexValidator(regex=r"^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$"),
        ),
    )
    description = models.CharField(
        verbose_name="Описание бота",
        max_length=constants.DESCRIPTION_LENGTH,
        blank=True,
    )
    api_key = models.CharField(
        verbose_name="Ключ API", max_length=constants.API_KEY_LENGTH, blank=True
    )
    api_url = models.URLField(
        verbose_name="Адрес API", max_length=constants.API_URL_LENGTH, blank=True
    )
    api_availability = models.BooleanField(
        verbose_name="Доступность API", blank=True, default=False
    )
    bot_state = models.CharField(
        verbose_name="Статус бота",
        max_length=7,
        choices=BotState,
        default=BotState.DRAFT,
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    started_at = models.DateTimeField(
        verbose_name="Дата последнего запуска бота", blank=True, null=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Телеграм бот"
        verbose_name_plural = "Телеграм боты"

    def __str__(self) -> str:
        """Строковое отображение объекта модели телеграм бота в виде его имени."""
        return self.name

    def save(self, *args, **kwargs) -> None:
        """
        Модернизированный метод сохранения объекта телеграм бота.
        Если объект модели создается, то к ней дополнительно создается действие /start.

        """
        created: bool = not self.pk
        super().save(*args, **kwargs)
        if created:
            TelegramBotAction.objects.create(
                telegram_bot=self,
                name="Старт",
                command_keyword="/start",
                position=1,
                is_active=True,
            )

    @property
    def is_started(self) -> bool:
        """
        Свойство телеграм бота.
        Возвращает True если бот запущен,
        возвращает False, если бот остановлен.
        """
        return (
            self.bot_state == self.BotState.RUNNING
            or self.bot_state == self.BotState.ERROR
        )


class TelegramBotAction(models.Model):
    """Модель действия для телеграм бота."""

    telegram_bot = models.ForeignKey(
        to="TelegramBot",
        verbose_name="Телеграм бот",
        on_delete=models.CASCADE,
        related_name="actions",
    )
    name = models.CharField(
        verbose_name="Название действия",
        max_length=constants.ACTION_NAME_LENGTH,
    )
    description = models.CharField(
        verbose_name="Описание действия",
        max_length=constants.DESCRIPTION_LENGTH,
        blank=True,
    )
    command_keyword = models.CharField(
        verbose_name="Текст команды",
        max_length=33,
        help_text="команда должна начинаться с / и содержать только латинские "
        "буквы, цифры и нижнее подчеркивание _, макс. длина 32 символа",
        validators=(validators.RegexValidator(regex=r"^/[a-zA-Z0-9_]{1,32}$"),),
    )
    message = models.CharField(
        verbose_name="Текст сообщения", max_length=constants.MESSAGE_LENGTH, blank=True
    )
    api_url = models.URLField(
        verbose_name="Адрес API", max_length=constants.API_URL_LENGTH, blank=True
    )
    api_key = models.CharField(
        verbose_name="Ключ API", max_length=constants.API_KEY_LENGTH, blank=True
    )
    position = models.SmallIntegerField(
        "Номер действия",
        validators=(
            validators.MinValueValidator(1),
            validators.MaxValueValidator(constants.MAX_POSITIONS),
        ),
    )
    is_active = models.BooleanField(verbose_name="Вкл/выкл")
    next_action = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        related_name="previous_actions",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"
        unique_together = (
            "telegram_bot",
            "position",
        )

    def __str__(self) -> str:
        """Строковое отображение объекта модели действия бота в виде его имени."""
        return self.name


def bot_directory_path(instance, filename: str) -> str:
    """Создаёт путь для сохраняемого файла в зависимости от id телеграм бота."""
    return f"bots/{instance.telegram_action.telegram_bot.id}/files/{filename}"


class TelegramBotFile(models.Model):
    """Модель для хранения файла для действия телеграм бота."""

    telegram_action = models.ForeignKey(
        to="TelegramBotAction",
        on_delete=models.CASCADE,
        related_name="files",
    )
    file = models.FileField(verbose_name="Файл", upload_to=bot_directory_path)

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self) -> str:
        """Строковое отображение объекта модели файла действия в виде его имени."""
        return self.file.name
