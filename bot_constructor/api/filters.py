# type:ignore
from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from apps.bot_management.models import TelegramBot


class TelegramBotFilter(filters.FilterSet):
    """Фильтр для представления телеграм ботов."""

    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")
    is_started = filters.BooleanFilter(
        field_name="is_started", method="filter_is_started"
    )

    class Meta:
        model = TelegramBot
        fields = (
            "name",
            "is_started",
            "created_at",
            "started_at",
            "bot_state",
        )

    def filter_is_started(self, queryset: QuerySet, _name: str, value: bool):
        """Фильтр для свойства is_started."""
        if value:
            return queryset.filter(
                Q(bot_state__exact=TelegramBot.BotState.RUNNING)
                | Q(bot_state__exact=TelegramBot.BotState.ERROR)
            )
        return queryset.filter(
            Q(bot_state__exact=TelegramBot.BotState.STOPPED)
            | Q(bot_state__exact=TelegramBot.BotState.DRAFT)
        )
