from django.contrib import admin

from .models import (  # type: ignore
    Header,
    TelegramBot,
    TelegramBotAction,
    TelegramBotFile,
    Variable,
)


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("name", "bot_state")


@admin.register(TelegramBotAction)
class TelegramBotActionAdmin(admin.ModelAdmin):
    pass


@admin.register(TelegramBotFile)
class TelegramBotFileAdmin(admin.ModelAdmin):
    pass


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    pass


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    pass
