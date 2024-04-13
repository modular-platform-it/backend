from django.urls import include, path
from rest_framework_nested import routers

from api.views import (
    TelegramBotViewSet,
    TelegramBotActionViewSet,
    TelegramBotActionFileViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register("bots", TelegramBotViewSet)
actions_router = routers.NestedDefaultRouter(
    router_v1, "bots", lookup="telegram_bot"
)
actions_router.register(
    "actions", TelegramBotActionViewSet, basename="telegram_bot-actions"
)
files_router = routers.NestedDefaultRouter(
    actions_router, "actions", lookup="telegram_action"
)
files_router.register(
    "files", TelegramBotActionFileViewSet, basename="telegram_bot_action-files"
)

urlpatterns = [
    path("api/", include(router_v1.urls)),
    path("api/", include(actions_router.urls)),
    path("api/", include(files_router.urls)),
]
