from decimal import Decimal
from abc import ABC, abstractmethod
from app.models import Car
from app.repo.common_objects import Operator

class CarsRepository(ABC):
    @abstractmethod
    def all_cars(self) -> [Car]:
        pass

    @abstractmethod
    def with_mileage(self, operator: Operator, value: int) -> [Car]:
        pass

    @abstractmethod
    def with_price_between(self, price_min: Decimal, price_max: Decimal) -> [Car]:
        pass