from django.contrib import admin

from .models import TelegramBot, TelegramBotAction  # type: ignore


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("name", "bot_state")


@admin.register(TelegramBotAction)
class TelegramBotActionAdmin(admin.ModelAdmin):
    pass
