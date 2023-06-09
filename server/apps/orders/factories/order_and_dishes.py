from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from apps.orders.models import OrderAndDishes
from apps.users.factories import EmployeeFactory

from . import DishFactory, OrderFactory


class OrderAndDishesFactory(DjangoModelFactory):
    """Factory for OrderAndDishes instance."""

    status = fuzzy.FuzzyChoice(
        [item[0] for item in OrderAndDishes.Statuses.choices],
    )
    order = SubFactory(
        OrderFactory,
    )
    dish = SubFactory(
        DishFactory,
    )
    comment = Faker(
        "text",
        max_nb_chars=30,
    )
    employee = SubFactory(
        EmployeeFactory,
    )

    class Meta:
        model = OrderAndDishes
