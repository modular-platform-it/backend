# from http import HTTPStatus

# from django.test import Client, TestCase
# from django.urls import reverse


# class AllauthURLTests(TestCase):

#     def setUp(self) -> None:
#         self.client: Client = Client()
#         self.login_url: str = reverse("login")

#     def test_login_url_and_cookies(self) -> None:
#         """Проверка доступности адреса /accounts/login/ и наличия куки."""
#         response = self.client.post(
#             self.login_url,
#             {
#                 "email": "test@test.ru",  # pragma: allowlist secret
#                 "password": "password",  # pragma: allowlist secret
#             },
#             follow=True,
#         )
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertContains(response, "/accounts/login/")
#         self.assertIsNotNone(
#             self.client.cookies["csrftoken"], f"Куки 'csrftoken' не найдены"
#         )

#     def test_login_fieldss(self) -> None:
#         """Проверка обязательных полей при входе."""
#         response = self.client.post(self.login_url, {"email": "", "password": ""})
#         form = response.context["form"]
#         self.assertTrue(form.has_error("email", "required"))
#         self.assertTrue(form.has_error("password", "required"))
