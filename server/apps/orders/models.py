from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


def get_directory_path(instance, filename) -> str:
    return (
        f"dishes/{instance.dish.name.replace(' ', '_')}"
        f"_{instance.dish.id}/{filename}"
    )


def validate_arrival_time(arrival_time) -> None:
    if timezone.now() >= arrival_time:
        raise ValidationError(
            "Время прихода не может быть раньше текущего времени",
        )


class Category(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="Название",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return f"Category {self.name}"


class Dish(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="Категория",
    )
    name = models.CharField(
        max_length=128,
        verbose_name="Название",
    )
    description = models.TextField(
        verbose_name="Полное описание",
    )
    short_description = models.TextField(
        verbose_name="Краткое описание",
    )
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена",
    )
    compound = models.TextField(
        verbose_name="Состав",
    )
    weight = models.DecimalField(
        max_digits=11,
        decimal_places=3,
        validators=[MinValueValidator(0)],
        verbose_name="Вес блюда",
    )
    reviews = models.ManyToManyField(
        "reviews.Review",
        related_name="dish",
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self) -> str:
        return f"Dish {self.name} {self.category} {self.price} {self.description}"


class DishImages(models.Model):
    image = models.ImageField(
        upload_to=get_directory_path,
        verbose_name="Картинка",
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Блюдо",
    )

    class Meta:
        verbose_name = "Картинка блюда"
        verbose_name_plural = "Картинки блюд"

    def __str__(self) -> str:
        return f"Order {self.dish}"


class Order(models.Model):

    class Statuses(models.TextChoices):
        WAITING_FOR_COOKING = "WAITING_FOR_COOKING", "Передано на кухню"
        COOKING = "COOKING", "Готовится"
        WAITING_FOR_DELIVERY = "WAITING_FOR_DELIVERY", "Ожидает доставки/готово к выдаче"
        IN_PROCESS_DELIVERY = "IN_PROCESS_DELIVERY", "В процессе доставки"
        DELIVERED = "DELIVERED", "Доставлен"
        FINISHED = "FINISHED", "Закрыт"
        CANCEL = "CANCEL", "Отменен"
        PAID = "PAID", "Оплачен"

    status = models.TextField(
        choices=Statuses.choices,
        default=Statuses.WAITING_FOR_COOKING,
        verbose_name="Статус заказа",
    )
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена",
    )
    comment = models.TextField(
        default="",
        verbose_name="Комментарий",
    )
    employee = models.ForeignKey(
        "users.Employee",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name="Сотрудник",
    )
    client = models.ForeignKey(
        "users.Client",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name="Клиент",
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"Order {self.price} {self.comment} {self.employee}"


class OrderAndDishes(models.Model):

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
        Order,
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="Заказ",
    )
    dish = models.ForeignKey(
        Dish,
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


class RestaurantAndOrder(models.Model):
    arrival_time = models.DateTimeField(
        validators=[validate_arrival_time],
        verbose_name="Время прибытия",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="restaurant_and_order",
        verbose_name="Заказ",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="restaurant_and_order",
        verbose_name="Ресторан",
    )
    place_number = models.PositiveIntegerField(
        verbose_name="Номер места",
    )

    class Meta:
        verbose_name = "Ресторан и заказ"
        verbose_name_plural = "Ресторан и заказы"

    def __str__(self) -> str:
        return f"RestaurantAndOrder {self.arrival_time} {self.order} {self.restaurant}"


class StopList(models.Model):
    dish = models.ForeignKey(
        Dish,
        related_name="stop_list",
        on_delete=models.CASCADE,
        verbose_name="Блюда",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="stop_list",
        verbose_name="Ресторан",
    )

    class Meta:
        verbose_name = "Стоп лист ресторана"
        verbose_name_plural = "Стоп листы ресторанов"

    def __str__(self) -> str:
        return f"StopList with dish: {self.dish}, restaurant: {self.restaurant}"
