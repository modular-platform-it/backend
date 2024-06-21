import apps.bot_management.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TelegramBot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Название бота"
                    ),
                ),
                (
                    "telegram_token",
                    models.CharField(
                        max_length=46,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$"
                            )
                        ],
                        verbose_name="Токен авторизации телеграм бота",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=1000, verbose_name="Описание бота"
                    ),
                ),
                (
                    "api_key",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Ключ API"
                    ),
                ),
                (
                    "api_url",
                    models.URLField(
                        blank=True, max_length=255, verbose_name="Адрес API"
                    ),
                ),
                (
                    "api_availability",
                    models.BooleanField(
                        blank=True, default=False, verbose_name="Доступность API"
                    ),
                ),
                (
                    "bot_state",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Черновик"),
                            ("RUNNING", "Запущен"),
                            ("STOPPED", "Остановлен"),
                            ("ERROR", "Ошибка"),
                        ],
                        default="DRAFT",
                        max_length=7,
                        verbose_name="Статус бота",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Дата создания"
                    ),
                ),
                (
                    "started_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Дата последнего запуска бота",
                    ),
                ),
            ],
            options={
                "verbose_name": "Телеграм бот",
                "verbose_name_plural": "Телеграм боты",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="TelegramBotAction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=20, verbose_name="Название действия"),
                ),
                (
                    "action_type",
                    models.CharField(
                        choices=[
                            ("GetListHandler", "Получение Списка"),
                            ("StopHandler", "Остановка"),
                            ("Handlers", "Старт"),
                            ("RandomWordLearnListHandler", "Словарик слов с переводом"),
                            ("GetItem", "Получение обьекта"),
                        ],
                        default="Handlers",
                        max_length=30,
                        verbose_name="Тип действия",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=1000, verbose_name="Описание действия"
                    ),
                ),
                (
                    "command_keyword",
                    models.CharField(
                        blank=True,
                        help_text="команда должна начинаться с / и содержать только латинские буквы, цифры и нижнее подчеркивание _, макс. длина 32 символа",
                        max_length=33,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^/[a-zA-Z0-9_]{1,32}$"
                            )
                        ],
                        verbose_name="Текст команды",
                    ),
                ),
                (
                    "message",
                    models.CharField(
                        blank=True,
                        max_length=1000,
                        null=True,
                        verbose_name="Текст сообщения",
                    ),
                ),
                (
                    "api_url",
                    models.URLField(
                        blank=True, max_length=255, verbose_name="Адрес API"
                    ),
                ),
                (
                    "api_key",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Ключ API"
                    ),
                ),
                (
                    "api_method",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("GET", "Get запрос"),
                            ("POST", "Post запрос"),
                            ("PATCH", "Patch запрос"),
                            ("DELETE", "Delete запрос"),
                            ("PUT", "Put запрос"),
                        ],
                        default="GET",
                        max_length=7,
                        verbose_name="Метод запроса к API",
                    ),
                ),
                (
                    "data",
                    models.JSONField(blank=True, null=True, verbose_name="Данные"),
                ),
                (
                    "position",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(30),
                        ],
                        verbose_name="Номер действия",
                    ),
                ),
                ("is_active", models.BooleanField(verbose_name="Вкл/выкл")),
                (
                    "next_action",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="previous_actions",
                        to="bot_management.telegrambotaction",
                    ),
                ),
                (
                    "telegram_bot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions",
                        to="bot_management.telegrambot",
                        verbose_name="Телеграм бот",
                    ),
                ),
            ],
            options={
                "verbose_name": "Действие",
                "verbose_name_plural": "Действия",
                "unique_together": {("telegram_bot", "position")},
            },
        ),
        migrations.CreateModel(
            name="Header",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="[a-zA-Z0-9-]{1,30}"
                            )
                        ],
                        verbose_name="Наименование заголовка",
                    ),
                ),
                (
                    "telegram_action",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="headers",
                        to="bot_management.telegrambotaction",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заголовок",
                "verbose_name_plural": "Заголовки",
            },
        ),
        migrations.CreateModel(
            name="TelegramBotFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to=apps.bot_management.models.bot_directory_path,
                        verbose_name="Файл",
                    ),
                ),
                (
                    "telegram_action",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="bot_management.telegrambotaction",
                    ),
                ),
            ],
            options={
                "verbose_name": "Файл",
                "verbose_name_plural": "Файлы",
            },
        ),
        migrations.CreateModel(
            name="Variable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="В названии используйте только латинские буквы и цифры, _ и -",
                        max_length=30,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^[a-zA-Z0-9_]{1,30}"
                            )
                        ],
                        verbose_name="Название переменной",
                    ),
                ),
                (
                    "variable_type",
                    models.CharField(
                        choices=[
                            ("INT", "Целое число"),
                            ("FLOAT", "Число с плавающей запятой"),
                            ("STRING", "Строка"),
                        ],
                        max_length=15,
                        verbose_name="Тип переменной",
                    ),
                ),
                (
                    "telegram_action",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variables",
                        to="bot_management.telegrambotaction",
                    ),
                ),
            ],
            options={
                "verbose_name": "Переменная",
                "verbose_name_plural": "Переменные",
            },
        ),
    ]
