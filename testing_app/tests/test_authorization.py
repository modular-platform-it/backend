from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class DjoserURLTests(TestCase):

    def setUp(self):
        self.user_info = self.generate_user_info()

    def generate_user_info(self):
        return {
            "password": "fake.password()",  # pragma: allowlist secret
            "username": "fake.user_name()",  # pragma: allowlist secret
        }

    def test_login_url(self):
        """Проверка доступности адреса для входа."""
        user_info = self.generate_user_info()
        url = reverse("login")
        data = {
            "password": user_info["password"],
            "username": user_info["username"],
        }
        response = self.client.post(url, data)
        self.assertTrue(response.status_code, HTTPStatus.OK)

    def test_login_fields(self) -> None:
        """Проверка обязательных полей при входе."""
        response = self.client.post(
            "/auth/token/login/", {"password": "", "username": ""}
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.json()["non_field_errors"][0],
            "Невозможно войти с предоставленными учетными данными.",
        )
        self.assertEqual(
            response.json()["non_field_errors"][-1],
            "Невозможно войти с предоставленными учетными данными.",
        )

    def test_logout_url(self):
        """Проверка доступности адреса для выхода."""
        url = reverse("logout")
        response = self.client.post(url)
        self.assertTrue(response.status_code, HTTPStatus.NO_CONTENT)
