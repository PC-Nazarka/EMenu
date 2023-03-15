from django.db import models


class OrderAndDish(models.Model):
    class Statuses(models.TextChoices):
        WAITING_FOR_COOKING = "WAITING_FOR_COOKING", "Ожидает готовки"
        COOKING = "COOKING", "Готовится"
        DONE = "DONE", "Готово"
        DELIVERED = "DELIVERED", "Выдано"

    status = models.TextField(
        choices=Statuses.choices,
        default=Statuses.WAITING_FOR_COOKING,
        verbose_name="Статус блюда",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="Заказ",
    )
    dish = models.ForeignKey(
        "orders.Dish",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Блюдо",
    )
    employee = models.ForeignKey(
        "users.Employee",
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="dishes",
        verbose_name="Исполняющий сотрудник",
    )
    comment = models.TextField(
        default="",
        verbose_name="Комментарий",
    )

    class Meta:
        verbose_name = "Заказ и блюдо"
        verbose_name_plural = "Заказы и блюда"

    def __str__(self) -> str:
        return f"OrderAndDish {self.order} {self.dish}"