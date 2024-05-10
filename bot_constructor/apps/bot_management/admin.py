from django.contrib import admin

from .models import TelegramBot  # type: ignore


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("name", "bot_state")
