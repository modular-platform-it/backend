# Generated by Django 5.0.4 on 2024-04-23 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot_management", "0004_remove_telegrambot_is_started_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="telegrambot",
            name="api_key",
            field=models.CharField(blank=True, max_length=255, verbose_name="Ключ API"),
        ),
        migrations.AlterField(
            model_name="telegrambot",
            name="api_url",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Адрес API"
            ),
        ),
    ]
