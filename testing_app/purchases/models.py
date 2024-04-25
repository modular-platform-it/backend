from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Cart(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name="Название карточки",
        help_text="Введите название карточки",
    )
    measurement_unit = models.TextField(verbose_name="Единицы измерения")
    description = models.TextField()

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shoper",
        verbose_name="Покупатель",
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="purchase",
        verbose_name="Покупки",
    )

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        unique_together = [["cart", "user"]]

    def __str__(self) -> str:
        return f"{self.cart}"