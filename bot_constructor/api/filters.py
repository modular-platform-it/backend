from django_filters import rest_framework as filters

from apps.bot_management.models import TelegramBot


class TelegramBotFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")
    # is_started = filters.BooleanFilter(field_name='is_started')

    class Meta:
        model = TelegramBot
        fields = (
            "name",
            "is_started",
            "created_at",
            "started_at",
            "bot_state",
        )
