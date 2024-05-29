from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from purchases.constants import (
    CART_DESCRIPTION,
    CART_MEASUREMENT_UNIT,
    CART_NAME,
    PASSWORD,
    USER_USERNAME,
)
from purchases.models import Cart, ShoppingCart


class CartViewSetTests(TestCase):

    def test_get_cart_list(self):
        """Проверка получения списка карточек для авторизованного пользователя."""
        self.user = get_user_model().objects.create_user(username=USER_USERNAME)
        self.client.login(username=USER_USERNAME, password=PASSWORD)
        response = self.client.get("/api/carts/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, list)

    def test_get_cart_detail(self):
        """Проверка получения карточки товара по id для авторизованного пользователя."""
        self.user = get_user_model().objects.create_user(username=USER_USERNAME)
        self.client.login(username=USER_USERNAME, password=PASSWORD)
        cart = Cart.objects.create(
            name=CART_NAME,
            description=CART_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )
        response = self.client.get(f"/api/carts/{cart.id}/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, dict)


class ShoppingCartViewSetTests(TestCase):

    def test_get_shoppingcart_list(self):
        """Проверка получения списка покупок для авторизованного пользователя."""
        self.user = get_user_model().objects.create_user(username=USER_USERNAME)
        self.client.login(username=USER_USERNAME, password=PASSWORD)
        response = self.client.get("/api/shoppingCart/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, list)

    def test_get_cart_detail(self):
        """Проверка получения списка покупок по id для авторизованного пользователя."""
        self.user = get_user_model().objects.create_user(username=USER_USERNAME)
        self.client.login(username=USER_USERNAME, password=PASSWORD)
        cart = Cart.objects.create(
            name=CART_NAME,
            description=CART_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )
        shopping_cart = ShoppingCart.objects.create(
            cart=cart, date_added=timezone.now(), user=self.user
        )
        response = self.client.get(f"/api/shoppingCart/{shopping_cart.id}/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, dict)
