import pytest
from decimal import Decimal

from app.models import Car, Color, Component

from app.repo import LocalCarsRepository
from app.repo.common_objects import Operator




class TestLocalCarsRepository:
    cars_collection: [Car] = [
    Car('BMW', Decimal('100'), Color.WHITE, 100, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg"),
    Car('AUDI', Decimal('101'), Color.WHITE, 101, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_c1UuDL1pc55A.jpg")]

    local_cars_repository_instance = LocalCarsRepository(cars_collection)
    def test_all_cars(self) -> None:

        assert self.local_cars_repository_instance.all_cars() == self.cars_collection

    @pytest.mark.parametrize("operator, value, expected_value", [
        [Operator.EQ , 100, [cars_collection[0]]],
        [Operator.NE , 100, [cars_collection[1]]],
        [Operator.GT , 100, [cars_collection[1]]],
        [Operator.LT , 101, [cars_collection[0]]],
        [Operator.GE , 100, cars_collection],
        [Operator.LE , 101, cars_collection],
        ['FAKE_OPERATOR', 100, {"exception": TypeError, "error_msg": 'Invalid operator'}]
    ])
    def test_with_mileage(self, operator, value, expected_value) -> None:
        if isinstance(operator, Operator):
            assert self.local_cars_repository_instance.with_mileage(operator, value) == expected_value
        else:
            with pytest.raises(expected_value['exception']) as e:
                self.local_cars_repository_instance.with_mileage(operator, value)
            assert e.value.args[0] == expected_value['error_msg']

    @pytest.mark.parametrize('price_min, price_max, expected_value', [
        (Decimal('100.00'), Decimal('101.00'), cars_collection),
        (Decimal('99.99'), Decimal('101.01'), cars_collection),
        (Decimal('100'), Decimal('100'), [cars_collection[0]]),
        (Decimal('-1'), Decimal('100'),  {"exception": ValueError, "error_msg": 'Price range cannot be negative'})
    ])
    def test_with_price_between(self, price_min, price_max, expected_value) -> None:
        if isinstance(expected_value, list):
            assert self.local_cars_repository_instance.with_price_between(price_min, price_max) == expected_value
        else:
            with pytest.raises(expected_value['exception']) as e:
                self.local_cars_repository_instance.with_price_between(price_min, price_max)
            assert e.value.args[0] == expected_value['error_msg']
