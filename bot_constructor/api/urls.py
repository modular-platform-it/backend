from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_nested import routers

from api.views import (
    HeaderViewSet,
    TelegramBotActionFileViewSet,
    TelegramBotActionViewSet,
    TelegramBotViewSet,
    TokenDestroyView,
    VariableViewSet,
)

from .drf_spectacular.drf_views import swagger_login, swagger_logout

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
    path("auth/token/logout/", TokenDestroyView.as_view()),
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
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
