from djoser.views import TokenCreateView

from api.views import (
    CustomTokenDestroyView,
    HeaderViewSet,
    TelegramBotActionFileViewSet,
    TelegramBotActionViewSet,
    TelegramBotViewSet,
    VariableViewSet,
)
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_nested import routers

router_v1 = routers.DefaultRouter()
router_v1.register("bots", TelegramBotViewSet)
actions_router_v1 = routers.NestedDefaultRouter(
    router_v1, "bots", lookup="telegram_bot"
)
actions_router_v1.register(
    "actions", TelegramBotActionViewSet, basename="telegram_bot-actions"
)
files_router_v1 = routers.NestedDefaultRouter(
    actions_router_v1, "actions", lookup="telegram_action"
)
files_router_v1.register(
    "files", TelegramBotActionFileViewSet, basename="telegram_bot_action-files"
)
variables_router_v1 = routers.NestedDefaultRouter(
    actions_router_v1, "actions", lookup="telegram_action"
)
variables_router_v1.register(
    "variables", VariableViewSet, basename="telegram_bot_action-variables"
)
headers_router_v1 = routers.NestedDefaultRouter(
    actions_router_v1, "actions", lookup="telegram_action"
)
headers_router_v1.register(
    "headers", HeaderViewSet, basename="telegram_bot_action-headers"
)

urlpatterns = [
    path("", include("djoser.urls")),
    path("auth/token/login/?$", TokenCreateView.as_view(), name="login"),
    path("auth/token/logout/?$", CustomTokenDestroyView.as_view(), name="logout"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path("", include(router_v1.urls)),
    path("", include(actions_router_v1.urls)),
    path("", include(files_router_v1.urls)),
    path("", include(variables_router_v1.urls)),
    path("", include(headers_router_v1.urls)),
]
