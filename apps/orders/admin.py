from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Class representation of Category model in admin panel."""

    list_display = (
        "id",
        "name",
    )


@admin.register(models.Dish)
class DishAdmin(admin.ModelAdmin):
    """Class representation of Dish model in admin panel."""

    list_display = (
        "id",
        "category",
        "name",
        "description",
        "price",
    )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Class representation of Order model in admin panel."""

    list_display = (
        "id",
        "price",
        "comment",
        "employee",
        "place_number",
    )


@admin.register(models.OrderDishes)
class OrderDishesAdmin(admin.ModelAdmin):
    """Class representation of OrderDishes model in admin panel."""

    list_display = (
        "id",
        "order",
        "dish",
    )


@admin.register(models.OrderClient)
class OrderClientAdmin(admin.ModelAdmin):
    """Class representation of OrderClient model in admin panel."""

    list_display = (
        "id",
        "client",
        "order",
    )


@admin.register(models.DishImages)
class DishImagesAdmin(admin.ModelAdmin):
    """Class representation of DishImages model in admin panel."""

    list_display = (
        "id",
        "image",
        "dish",
    )


@admin.register(models.RestaurantAndOrder)
class RestaurantAndOrderAdmin(admin.ModelAdmin):
    """Class representation of RestaurantAndOrder model in admin panel."""

    list_display = (
        "id",
        "arrival_time",
        "order",
        "restaurant",
    )
