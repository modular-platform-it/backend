# type: ignore
from allauth.account.views import LoginView, LogoutView
from api.views import (
    TelegramBotActionFileViewSet,
    TelegramBotActionViewSet,
    TelegramBotViewSet,
)
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_nested import routers

router_v1 = routers.DefaultRouter()
router_v1.register("bots", TelegramBotViewSet)
actions_router = routers.NestedDefaultRouter(router_v1, "bots", lookup="telegram_bot")
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
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("", include(router_v1.urls)),
    path("", include(actions_router.urls)),
    path("", include(files_router.urls)),
]
