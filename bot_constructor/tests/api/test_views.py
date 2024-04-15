import os
import shutil

from apps.bot_management.models import TelegramBot, TelegramBotAction, TelegramBotFile
from django.urls import reverse
from factory_data.factories import (
    FS_STORAGE,
    TelegramBotActionFactory,
    TelegramBotFactory,
    TelegramBotFileFactory,
)
from rest_framework import status
from rest_framework.test import APITestCase


class TestTelegramBotView(APITestCase):
    def setUp(self) -> None:
        self.telegram_bot = TelegramBotFactory.build()
        self.url_list = reverse("telegrambot-list")
        self.url_detail = "telegrambot-detail"
        return super().setUp()

    def test_telegram_bot_list_view(self):
        telegram_bots = TelegramBotFactory.create_batch(5)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        for telegram_bot in telegram_bots:
            self.assertContains(response, telegram_bot.name)

    def test_telegram_bot_create_view(self):
        count = TelegramBot.objects.count()
        response = self.client.post(
            self.url_list,
            {
                "name": self.telegram_bot.name,
                "telegram_token": self.telegram_bot.telegram_token,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.telegram_bot.name, response.data.get("name"))
        self.assertEqual(count + 1, TelegramBot.objects.count())

    def test_telegram_bot_detail_view(self):
        telegram_bot = TelegramBotFactory.create()
        response = self.client.get(
            reverse("telegrambot-detail", kwargs={"pk": telegram_bot.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_telegram_bot_delete_view(self):
        telegram_bot: TelegramBot = TelegramBotFactory.create()
        count = TelegramBot.objects.count()
        response = self.client.delete(
            reverse("telegrambot-detail", kwargs={"pk": telegram_bot.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(count - 1, TelegramBot.objects.count())

    def test_telegram_bot_update_view(self):
        telegram_bot: TelegramBot = TelegramBotFactory.create()
        new_telegram_bot: TelegramBot = TelegramBotFactory.build()
        response = self.client.put(
            reverse(self.url_detail, kwargs={"pk": telegram_bot.id}),
            data={
                "name": new_telegram_bot.name,
                "telegram_token": new_telegram_bot.telegram_token,
                "api_key": new_telegram_bot.api_key,
                "api_url": new_telegram_bot.api_url,
            },
        )
        updated_bot = TelegramBot.objects.get(id=telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_telegram_bot.name, updated_bot.name)
        self.assertEqual(new_telegram_bot.telegram_token, updated_bot.telegram_token)
        self.assertEqual(new_telegram_bot.api_url, updated_bot.api_url)
        self.assertEqual(new_telegram_bot.api_key, updated_bot.api_key)


class TestTelegramBotActionView(APITestCase):
    def setUp(self) -> None:
        self.telegram_bot = TelegramBotFactory.create()
        self.telegram_action = TelegramBotActionFactory.create(
            telegram_bot=self.telegram_bot
        )
        self.url_list = "telegram_bot-actions-list"
        self.url_detail = "telegram_bot-actions-detail"
        return super().setUp()

    def test_telegram_bot_action_list_view(self):
        telegram_actions = TelegramBotActionFactory.create_batch(
            5, telegram_bot=self.telegram_bot
        )
        response = self.client.get(
            reverse(self.url_list, kwargs={"telegram_bot_pk": self.telegram_bot.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        for telegram_action in telegram_actions:
            self.assertContains(response, telegram_action.name)

    def test_telegram_bot_action_create_view(self):
        count = TelegramBotAction.objects.count()
        telegram_action: TelegramBotAction = TelegramBotActionFactory.build(
            telegram_bot=self.telegram_bot
        )
        response = self.client.post(
            reverse(self.url_list, kwargs={"telegram_bot_pk": self.telegram_bot.id}),
            data={
                "name": telegram_action.name,
                "telegram_bot": telegram_action.telegram_bot.id,
                "message": telegram_action.message,
                "position": telegram_action.position,
                "is_active": telegram_action.is_active,
                "command_keyword": telegram_action.command_keyword,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(telegram_action.name, response.data.get("name"))
        self.assertEqual(count + 1, TelegramBotAction.objects.count())

    def test_telegram_bot_action_detail_view(self):
        response = self.client.get(
            reverse(
                self.url_detail,
                kwargs={
                    "pk": self.telegram_action.id,
                    "telegram_bot_pk": self.telegram_bot.id,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_telegram_bot_action_delete_view(self):
        telegram_action: TelegramBotAction = TelegramBotActionFactory.create(
            telegram_bot=self.telegram_bot
        )
        count = TelegramBotAction.objects.count()
        response = self.client.delete(
            reverse(
                self.url_detail,
                kwargs={
                    "pk": telegram_action.id,
                    "telegram_bot_pk": self.telegram_bot.id,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(count - 1, TelegramBotAction.objects.count())

    def test_telegram_bot_action_update_view(self):
        telegram_bot: TelegramBot = TelegramBotFactory.create()
        telegram_action: TelegramBotAction = TelegramBotActionFactory.create(
            telegram_bot=telegram_bot
        )
        new_telegram_action: TelegramBotAction = TelegramBotActionFactory.build(
            telegram_bot=telegram_bot
        )
        response = self.client.put(
            reverse(
                self.url_detail,
                kwargs={
                    "pk": telegram_action.id,
                    "telegram_bot_pk": telegram_bot.id,
                },
            ),
            data={
                "telegram_bot": telegram_bot.id,
                "name": new_telegram_action.name,
                "command_keyword": new_telegram_action.command_keyword,
                "message": new_telegram_action.message,
                "position": new_telegram_action.position,
                "is_active": new_telegram_action.is_active,
            },
        )
        updated_action = TelegramBotAction.objects.get(
            id=telegram_action.id, telegram_bot=telegram_bot.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_telegram_action.name, updated_action.name)
        self.assertEqual(
            new_telegram_action.command_keyword, updated_action.command_keyword
        )
        self.assertEqual(new_telegram_action.message, updated_action.message)
        self.assertEqual(new_telegram_action.position, updated_action.position)
        self.assertEqual(new_telegram_action.is_active, updated_action.is_active)


class TestTelegramBotFileView(APITestCase):
    def setUp(self) -> None:
        self.telegram_bot = TelegramBotFactory.create()
        self.telegram_action = TelegramBotActionFactory.create(
            telegram_bot=self.telegram_bot
        )
        self.telegram_file = TelegramBotFileFactory(
            telegram_action=self.telegram_action
        )
        self.url_list = "telegram_bot_action-files-list"
        self.url_detail = "telegram_bot_action-files-detail"
        return super().setUp()

    def test_telegram_bot_file_list_view(self):
        telegram_files = TelegramBotFileFactory.create_batch(
            5, telegram_action=self.telegram_action
        )
        response = self.client.get(
            reverse(
                self.url_list,
                kwargs={
                    "telegram_bot_pk": self.telegram_bot.id,
                    "telegram_action_pk": self.telegram_action.id,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        for telegram_file in telegram_files:
            self.assertContains(response, telegram_file.id)

    def test_telegram_bot_file_create_view(self):
        count = TelegramBotFile.objects.count()
        telegram_file: TelegramBotFile = TelegramBotFileFactory.build(
            telegram_action=self.telegram_action
        )
        response = self.client.post(
            reverse(
                self.url_list,
                kwargs={
                    "telegram_bot_pk": self.telegram_bot.id,
                    "telegram_action_pk": self.telegram_action.id,
                },
            ),
            data={
                "telegram_action": telegram_file.telegram_action.id,
                "file": telegram_file.file,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count + 1, TelegramBotFile.objects.count())

    def test_telegram_bot_action_detail_view(self):
        response = self.client.get(
            reverse(
                self.url_detail,
                kwargs={
                    "pk": self.telegram_file.id,
                    "telegram_bot_pk": self.telegram_bot.id,
                    "telegram_action_pk": self.telegram_action.id,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.telegram_file.id)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(FS_STORAGE.root_path):
            shutil.rmtree(FS_STORAGE.root_path, ignore_errors=True)
        super().tearDownClass()
