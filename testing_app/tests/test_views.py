from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from purchases.constants import (
    CART_DESCRIPTION,
    CART_NEW_DESCRIPTION,
    CART_MEASUREMENT_UNIT,
    CART_NAME,
    CART_NEW_NAME,
    PASSWORD,
    USER_USERNAME,
)
from purchases.models import Cart, ShoppingCart


class CartViewSetTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=USER_USERNAME, password=PASSWORD
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_cart_list(self):
        """Проверка получения списка карточек для авторизованного пользователя."""
        response = self.client.get("/api/carts/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, list)

    def test_get_cart_detail(self):
        """Проверка получения карточки товара по id для авторизованного пользователя."""
        cart = Cart.objects.create(
            name=CART_NAME,
            description=CART_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )
        response = self.client.get(f"/api/carts/{cart.id}/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, dict)

    def test_create_cart(self):
        """Проверка создания карточки товара авторизованным пользователем"""
        data = {
            "name": CART_NAME,
            "description": CART_DESCRIPTION,
            "measurement_unit": CART_MEASUREMENT_UNIT,
        }
        response = self.client.post("/api/carts/", data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIsInstance(response.data, dict)

    def test_delete_cart(self):
        """Проверка удаления карточки товара авторизованным пользователем"""
        cart = Cart.objects.create(
            name=CART_NAME,
            description=CART_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )
        response = self.client.delete(f"/api/carts/{cart.id}/")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertFalse(ShoppingCart.objects.filter(id=cart.id).exists())

    def test_update_cart(self):
        """Проверка обновления карточки товара авторизованным пользователем"""
        cart = Cart.objects.create(
            name=CART_NAME,
            description=CART_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )
        new_name = CART_NEW_NAME
        new_description = CART_NEW_DESCRIPTION
        data = {
            "name": new_name,
            "description": new_description,
            "measurement_unit": CART_MEASUREMENT_UNIT,
        }
        response = self.client.put(f"/api/carts/{cart.id}/", data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["name"], new_name)
        self.assertEqual(response.data["description"], new_description)
        cart.refresh_from_db()
        self.assertEqual(cart.name, new_name)
        self.assertEqual(cart.description, new_description)


class ShoppingCartViewSetTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=USER_USERNAME, password=PASSWORD
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_shoppingcart_list(self):
        """Проверка получения списка покупок для авторизованного пользователя."""
        response = self.client.get("/api/shoppingCart/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, list)

    def test_get_shoppingcart_detail(self):
        """Проверка получения списка покупок по id для авторизованного пользователя."""
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

    def test_create_shoppingcart(self):
        """Проверка добавления товара в корзину авторизованным пользователем"""
        cart = Cart.objects.create(
            name=CART_NAME,
            description=CART_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )
        data = {
            "cart": cart.id,
        }
        response = self.client.post("/api/shoppingCart/", data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIsInstance(response.data, dict)

    def test_delete_shoppingcart(self):
        """Проверка удаления товара из корзины авторизованным пользователем"""
        cart = Cart.objects.create(
            name=CART_NAME,
            description=CART_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )
        shopping_cart = ShoppingCart.objects.create(
            cart=cart, date_added=timezone.now(), user=self.user
        )
        response = self.client.delete(f"/api/shoppingCart/{shopping_cart.id}/")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertFalse(ShoppingCart.objects.filter(id=shopping_cart.id).exists())

    def test_update_shoppingcart(self):
        """Проверка обновления товара в корзине авторизованным пользователем"""
        cart = Cart.objects.create(
            name=CART_NAME,
            description=CART_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )
        shopping_cart = ShoppingCart.objects.create(
            cart=cart, date_added=timezone.now(), user=self.user
        )
        new_cart = Cart.objects.create(
            name=CART_NEW_NAME,
            description=CART_NEW_DESCRIPTION,
            measurement_unit=CART_MEASUREMENT_UNIT,
        )

        data = {
            "cart": new_cart.id,
        }
        response = self.client.put(f"/api/shoppingCart/{shopping_cart.id}/", data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["cart"], new_cart.id)
        shopping_cart.refresh_from_db()
        self.assertEqual(shopping_cart.cart.id, new_cart.id)
