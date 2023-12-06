import logging
from dataclasses import dataclass
from decimal import Decimal
from collections import defaultdict
from typing import Callable

from app.models import Car, Color, Component
from app.repo import CarsRepository, Operator
from app.service.common_objects import SortOrder

import logging
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class CarsService:
    """
    Service that provides data based on entities in repository
    Entities are Car objects that have couple of arguments: model, price, mileage, color, components
    """
    cars_repo: CarsRepository

    def all_cars(self) -> [Car]:
        """
        Returns list of all cars despite their characteristics
        """
        return self.cars_repo.all_cars()

    def all_sorted_by(self, attr_name: str, sort_order: SortOrder) -> [Car]:
        """
        Returns list of cars based on sorting by attribute in selected order
        attr_name: any of Car attribute, for example 'model'
        sort_order: SortOrder.ASC | SortOrder.DESC
        """
        reverse_flag = True if sort_order == SortOrder.DESC else False
        def sort_by_attr_in_order(sorting_fn: Callable) -> list[Car]:
            return sorted(
                [car for car in self.all_cars()],
                key=sorting_fn,
                reverse=reverse_flag)


        match attr_name:
            case 'model':
                return sort_by_attr_in_order(lambda c: c.model)

            case 'price':
                return sort_by_attr_in_order(lambda c: c.price)

            case 'color':
                return sort_by_attr_in_order(lambda c: c.color)

            case 'mileage':
                return sort_by_attr_in_order(lambda c: c.mileage)

            case 'components':
                return sort_by_attr_in_order(lambda c: c.components)

            case _:
                raise ValueError('Invalid attribute name')

    def _get_statistics_for_numeric_field(self, cars: [Car], filed_name: str) -> dict[str, float | int] | dict[
        str, Decimal]:
        match filed_name:
            case 'mileage':
                elements = [car.mileage for car in cars]
            case 'price':
                elements = [car.price for car in cars]
            case _:
                raise ValueError('Invalid field name')
        return {
            "min": min(elements),
            "max": max(elements),
            "avg": sum(elements) / len(elements)

        }

    def get_statistics_for_numeric_fields(self, filed_names: [str]) -> dict[str, dict[str, float]]:
        """
        User can provide table with numeric attributes names, for example ["price", "mileage"]
        Having that, method will return dict with attribute name as key, and dict with statistics as value =>
        {"avg": value, "min": value, "max": value}
        """
        all_cars = self.all_cars()
        return {name: self._get_statistics_for_numeric_field(all_cars, name) for name in filed_names}

    def with_mileage_gt(self, value: int) -> [Car]:
        """
        Returns cars with mileage greater then parameter
        """
        return self.cars_repo.with_mileage(Operator.GT, value)

    def cars_colors_map(self) -> dict[Color, [Car]]:
        """
        Returns dict with color as key, and list of cars with that color as a value
        """
        cars_colors_map = defaultdict(list)
        for car in self.all_cars():
            cars_colors_map[car.color].append(car)

        return dict(cars_colors_map)

    def models_with_most_expensive_cars(self) -> dict[str, [Car]]:
        """
        Returns dict with model as key and list of cars with that model as a value
        """
        def _get_most_expensive_cars(cars: [Car]) -> [Car]:
            max_price = max([c.price for c in cars])

            return [c for c in cars if c.price == max_price]

        models_with_most_expensive_cars = defaultdict(list)

        for car in sorted(self.all_cars(), key=lambda c: c.model, reverse=True):
            models_with_most_expensive_cars[car.model].append(car)

        return {model: _get_most_expensive_cars(cars) for model, cars in models_with_most_expensive_cars.items()}

    def most_expensive_cars(self) -> [Car]:
        """
        Returns list of one or more the most expensive cars
        """
        all_cars = self.all_cars()
        max_price = max([car.price for car in all_cars])
        return [car for car in all_cars if car.price == max_price]

    def cars_with_sorted_components(self) -> [Car]:
        """
        Returns all cars, but their components are sorted
        """
        all_cars = self.all_cars()
        for car in all_cars:
            car.components.sort()
        return all_cars

    def components_with_cars_map(self) -> dict[Component, [Car]]:
        """
        Returns dict with component name as key and list of cars having this component as value
        """
        component_cars_map = defaultdict(list)
        for car in self.all_cars():
            for component in car.components:
                component_cars_map[component].append(car)

        return dict(component_cars_map)

    def cars_with_price_in_range_sorted_by(self, price_range: tuple[Decimal], sort_attr: SortOrder) -> dict[
        Component, [Car]]:
        """
        Returns cars in price range sorted in particular order
        """
        return sorted(self.cars_repo.with_price_between(*price_range),
                      reverse=True if sort_attr == SortOrder.DESC else False, key=lambda c: c.price
                      )
