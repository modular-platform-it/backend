# Generated by Django 5.0.6 on 2024-05-31 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bot_management", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="header",
            options={"verbose_name": "Заголовок", "verbose_name_plural": "Заголовки"},
        ),
        migrations.AlterModelOptions(
            name="variable",
            options={"verbose_name": "Переменная", "verbose_name_plural": "Переменные"},
        ),
    ]
