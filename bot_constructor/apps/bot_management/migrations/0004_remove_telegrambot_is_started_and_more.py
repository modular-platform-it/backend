# Generated by Django 5.0.4 on 2024-04-23 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "bot_management",
            "0003_telegrambot_description_telegrambotaction_api_key_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="telegrambot",
            name="is_started",
        ),
        migrations.AddField(
            model_name="telegrambotaction",
            name="next_action",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="next_actions",
                to="bot_management.telegrambotaction",
            ),
        ),
    ]
