import pytest
from decimal import Decimal
from app.models import Car, Color, Component

class TestCar:
    car1: Car = Car('BMW', Decimal('100'), Color.WHITE, 100, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg")

    def test__str__(self) -> None:
        """
        Test of conversion to string
        """
        assert str(self.car1) == 'BMW, 100, WHITE, 100, [AC]'


    @pytest.mark.parametrize("min_mileage, max_mileage, expected_result", [
        (99, 101, True),
        (100, 101, True),
        (99, 100, True),
        (0, 1, False),
        (1, 0, {"exception": ValueError, "error_msg": 'Miles range is not correct'}),
        (0, '1', {"exception": TypeError, "error_msg": 'Unexpected type for mileage range arguments'}),
        ('0', 1, {"exception": TypeError, "error_msg": 'Unexpected type for mileage range arguments'})
    ])
    def test_has_milage_between_without_errors(self, min_mileage, max_mileage, expected_result) -> None:
        if type(expected_result) == bool:
            assert self.car1.has_mileage_between(min_mileage, max_mileage) == expected_result
        else:
            with pytest.raises(expected_result["exception"]) as e:
                self.car1.has_mileage_between(min_mileage, max_mileage)
            assert e.value.args[0] == expected_result["error_msg"]


    @pytest.mark.parametrize("min_price, max_price, expected_result", [
        (Decimal('99'), Decimal('101'), True),
        (Decimal('100.00'), Decimal('101'), True),
        (Decimal('99.00'), Decimal('100.00'), True),
        (Decimal('0'), Decimal('1'), False),
        (Decimal('1'), Decimal('0'), {"exception": ValueError, "error_msg": 'Price range is not correct'}),
        (Decimal('0'), '1', {"exception": TypeError, "error_msg": 'Unexpected type for price range arguments'}),
        ('0', Decimal('1'), {"exception": TypeError, "error_msg": 'Unexpected type for price range arguments'})
    ])
    def test_has_price_between(self, min_price, max_price, expected_result) -> None:
        if type(expected_result) == bool:
            assert self.car1.has_price_between(min_price, max_price) == expected_result
        else:
            with pytest.raises(expected_result["exception"]) as e:
                self.car1.has_price_between(min_price, max_price)
            assert e.value.args[0] == expected_result["error_msg"]


    def test_from_json_dict(self) -> None:
        assert Car.from_json_dict(
            {
                "model": "BMW",
                "price": "100",
                "color": "WHITE",
                "mileage": 100,
                "components": [
                    {"name": "AC"}
                ],
                "icon": "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg"
            }
        ) == self.car1

