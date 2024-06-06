from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CartViewSet, ShoppingCartViewSet

app_name = "api"

router_v1 = DefaultRouter()

router_v1.register("carts", CartViewSet, basename="carts")
router_v1.register("shoppingCart", ShoppingCartViewSet, basename="shoppingCart")

urlpatterns = [
    path("", include(router_v1.urls)),
]
