from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from purchases.constants import (
    CART_DESCRIPTION,
    CART_MEASUREMENT_UNIT,
    CART_NAME,
    USER_USERNAME,
)
from purchases.models import Cart, ShoppingCart


class CartModelTest(TestCase):
    """Тесты для модели карточки товара."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cart = Cart.objects.create(
            name=CART_NAME,
            measurement_unit=CART_MEASUREMENT_UNIT,
            description=CART_DESCRIPTION,
        )

    def test_string_representation(self) -> None:
        """Проверка строкового представления модели карточки товара."""
        self.assertEqual(self.cart.name, str(self.cart))


class ShoppingCartModelTest(TestCase):
    """Тесты для модели списка покупок."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username=USER_USERNAME)
        cls.cart = Cart.objects.create(
            name=CART_NAME,
            measurement_unit=CART_MEASUREMENT_UNIT,
            description=CART_DESCRIPTION,
        )
        cls.shoppingcart = ShoppingCart.objects.create(
            user=cls.user,
            cart=cls.cart,
            date_added=timezone.now(),
        )

    def test_string_representation(self) -> None:
        """Проверка строкового представления модели списка покупок."""
        self.assertEqual(self.cart.name, str(self.cart))
