from decimal import Decimal
from dataclasses import dataclass
from typing import Final

from app.models import Car
from app.repo.abc import CarsRepository
from app.repo.common_objects import Operator


@dataclass(frozen=True)
class LocalCarsRepository(CarsRepository):
    _cars: [Car]
    def all_cars(self) -> [Car]:
        return [car for car in self._cars]

    def with_mileage(self, operator: Operator, value: int) -> [Car]:
        MAX_MILEAGE: Final = 6_000_000

        match operator:
            case Operator.EQ:
                return [car for car in self.all_cars() if car.has_mileage_between(value, value)]

            case Operator.NE:
                return [car for car in self.all_cars() if not car.has_mileage_between(value, value)]

            case Operator.GT:
                return [car for car in self.all_cars() if car.has_mileage_between(value + 1, MAX_MILEAGE)]

            case Operator.LT:
                return [car for car in self.all_cars() if car.has_mileage_between(0, value - 1)]

            case Operator.GE:
                return [car for car in self.all_cars() if car.has_mileage_between(value, MAX_MILEAGE)]

            case Operator.LE:
                return [car for car in self.all_cars() if car.has_mileage_between(0, value)]

            case _:
                raise TypeError('Invalid operator')


    def with_price_between(self, price_min: Decimal, price_max: Decimal) -> [Car]:
        if price_min < 0 or price_max < 0:
            raise ValueError('Price range cannot be negative')
        return [car for car in self._cars if car.has_price_between(price_min, price_max)]