from dataclasses import dataclass
from typing import Self, Any
from decimal import Decimal
from enum import StrEnum, auto

class Color(StrEnum):
    WHITE = auto()
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    PINK = auto()
    ORANGE = auto()
    SILVER = auto()
    def __str__(self) -> str:
        return f'{self.name}'

    def __lt__(self, other):
        return self.name < other.name


@dataclass(frozen=True)
class Component:
    name: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(name=data['name'])

    def __str__(self) -> str:
        return f'{self.name}'

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __ne__(self, other) -> bool:
        return not self.name == other.name



@dataclass(frozen=True)
class Car:
    model: str
    price: Decimal
    color: Color
    mileage: int
    components: list[Component]
    icon: str

    def __str__(self) -> str:
        return f'{self.model}, {self.price}, {self.color}, {self.mileage}, {self.components}'

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict[str, Any]:
        return {
            'model': self.model,
            'price': str(self.price),
            'color': str(self.color.value),
            'components': [{'name': component.name} for component in self.components],
            'mileage': self.mileage,
            'icon': self.icon
        }


    def has_mileage_between(self, min_mileage: int, max_mileage: int) -> bool:
        if {type(min_mileage), type(max_mileage)} != {int}:
            raise TypeError('Unexpected type for mileage range arguments')

        if min_mileage > max_mileage:
            raise ValueError('Miles range is not correct')

        return min_mileage <= self.mileage <=max_mileage

    def has_price_between(self, min_price: Decimal, max_price: Decimal) -> bool:
        if {type(min_price), type(max_price)} != {Decimal}:
            raise TypeError('Unexpected type for price range arguments')

        if min_price > max_price:
            raise ValueError('Price range is not correct')

        return min_price <= self.price <= max_price

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            model=data['model'],
            price=Decimal(data['price']),
            color=Color[data['color'].upper()],
            mileage=data['mileage'],
            components = [Component.from_dict(component_data) for component_data in data['components']],
            icon=data['icon']
        )
