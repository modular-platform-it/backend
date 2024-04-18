# type:ignore
from apps.bot_management.models import TelegramBot
from django_filters import rest_framework as filters


class TelegramBotFilter(filters.FilterSet):
    """Фильтр для представления телеграм ботов."""

    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = TelegramBot
        fields = (
            "name",
            "is_started",
            "created_at",
            "started_at",
            "bot_state",
        )
