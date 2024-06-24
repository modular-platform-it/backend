from apps.bot_management import constants, regexps
from django.core import validators
from django.db import models
from django.db.models.functions import Upper
from django.utils import timezone


class TelegramBot(models.Model):
    """Модель телеграм бота."""
    _is_started = None

    class BotState(models.TextChoices):
        DRAFT = "DRAFT", "Черновик"
        RUNNING = "RUNNING", "Запущен"
        STOPPED = "STOPPED", "Остановлен"
        ERROR = "ERROR", "Ошибка"

    name = models.CharField(
        verbose_name="Название бота",
        max_length=constants.BOT_NAME_LENGTH,
        unique=True,
    )
    telegram_token = models.CharField(
        verbose_name="Токен авторизации телеграм бота",
        max_length=constants.TELEGRAM_TOKEN_LENGTH,
        unique=True,
        validators=(validators.RegexValidator(regex=regexps.TELEGRAM_TOKEN_REGEXP),),
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
    created_at = models.DateTimeField(
        verbose_name="Дата создания", default=timezone.now
    )
    started_at = models.DateTimeField(
        verbose_name="Дата последнего запуска бота", blank=True, null=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Телеграм бот"
        verbose_name_plural = "Телеграм боты"
        constraints = [models.UniqueConstraint(Upper("name"), name="unique_name")]

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
                action_type="Handlers",
                position=1,
                is_active=True,
                description="Что-то описано",
            )

    @property
    def is_started(self) -> bool:
        """
        Свойство телеграм бота.
        Возвращает True если бот запущен,
        возвращает False, если бот остановлен.
        """
        if self._is_started is None:
            self._is_started = (
                    self.bot_state == self.BotState.RUNNING
                    or self.bot_state == self.BotState.ERROR
            )

        return self._is_started

    @is_started.setter
    def is_started(self, attr):
        self._is_started = attr


class TelegramBotAction(models.Model):
    """Модель действия для телеграм бота."""

    # TODO разбить модель на отдельные виды
    class ActionType(models.TextChoices):
        GetListHandler = "GetListHandler", "Получение Списка"
        StopHandler = "StopHandler", "Остановка"
        Handlers = "Handlers", "Старт"
        RandomWordLearnListHandler = (
            "RandomWordLearnListHandler",
            "Словарик слов с переводом",
        )
        GetItem = "GetItem", "Получение объекта"
        RandomListHandler = (
            "RandomListHandler",
            "Список объектов и получение рандомного n Объектов",
        )
        GetJoke = "GetJoke", "Получить шутку"
        PostItem = "PostItem", "Отправить запрос"

    class APIMethodType(models.TextChoices):
        GET = "GET", "Get запрос"
        POST = "POST", "Post запрос"
        PATCH = "PATCH", "Patch запрос"
        DELETE = "DELETE", "Delete запрос"
        PUT = "PUT", "Put запрос"

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
    action_type = models.CharField(
        "Тип действия",
        choices=ActionType,
        max_length=constants.ACTION_TYPE_LENGTH,
        default=ActionType.Handlers,
    )
    description = models.CharField(
        verbose_name="Описание действия",
        max_length=constants.DESCRIPTION_LENGTH,
        blank=True,
    )
    command_keyword = models.CharField(
        verbose_name="Текст команды",
        max_length=constants.COMMAND_KEYWORD_LENGTH + 1,
        help_text="команда должна начинаться с / и содержать только латинские "
        "буквы, цифры и нижнее подчеркивание _, макс. длина 32 символа",
        validators=(validators.RegexValidator(regex=regexps.COMMAND_KEYWORD_REGEXP),),
        blank=True,
    )
    message = models.CharField(
        verbose_name="Текст сообщения",
        max_length=constants.MESSAGE_LENGTH,
        blank=True,
        default="",
    )
    api_url = models.URLField(
        verbose_name="Адрес API", max_length=constants.API_URL_LENGTH, blank=True
    )
    api_key = models.CharField(
        verbose_name="Ключ API", max_length=constants.API_KEY_LENGTH, blank=True
    )
    api_method = models.CharField(
        "Метод запроса к API",
        choices=APIMethodType,
        default=APIMethodType.GET,
        max_length=constants.METHOD_LENGTH,
        blank=True,
    )
    data = models.JSONField("Данные", blank=True, null=True)
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


class Variable(models.Model):
    """Модель для пользовательской переменной."""

    class VariableType(models.TextChoices):
        INT = "INT", "Целое число"
        FLOAT = "FLOAT", "Число с плавающей запятой"
        STRING = "STRING", "Строка"

    telegram_action = models.ForeignKey(
        TelegramBotAction, on_delete=models.CASCADE, related_name="variables"
    )
    name = models.CharField(
        "Название переменной",
        validators=(validators.RegexValidator(regex=regexps.VARIABLE_REGEXP),),
        max_length=constants.VARIABLE_LENGTH,
        help_text="В названии используйте только латинские буквы и цифры, _ и -",
    )
    variable_type = models.CharField(
        "Тип переменной",
        choices=VariableType,
        max_length=constants.VARIABLE_TYPE_LENGTH,
    )

    class Meta:
        verbose_name = "Переменная"
        verbose_name_plural = "Переменные"

    def __str__(self) -> str:
        """Строковое представление пользовательской переменной."""
        return self.name


class Header(models.Model):
    """Модель для пользовательского заголовка http запроса."""

    telegram_action = models.ForeignKey(
        TelegramBotAction, on_delete=models.CASCADE, related_name="headers"
    )
    name = models.CharField(
        "Наименование заголовка",
        max_length=constants.ACTION_NAME_LENGTH,
        validators=(validators.RegexValidator(regex=regexps.HEADER_REGEXP),),
    )

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"

    def __str__(self) -> str:
        """Строковое представление заголовка для пользовательского http запроса."""
        return self.name
