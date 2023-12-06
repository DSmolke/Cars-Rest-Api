import mock
from decimal import Decimal

import pytest

from app.models import Car, Color, Component
from app.service import CarsService
from app.service.common_objects import SortOrder


class TestCarsService:
    """
    Test all functionalities of CarsService by using database repo
    """
    cars = [
        Car('BMW', Decimal('100'), Color.WHITE, 100, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg"),
        Car('AUDI', Decimal('101'), Color.BLACK, 101, [Component('DC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_c1UuDL1pc55A.jpg")
    ]
    repo_mock = mock.Mock(name='repo_mock')
    repo_mock.all_cars.return_value = cars
    repo_mock.with_mileage.return_value = [cars[1]]
    repo_mock.with_price_between.return_value = cars


    cars_service_instance = CarsService(repo_mock)

    def test_all_cars(self) -> None:
        assert self.cars_service_instance.all_cars() == self.cars

    def test_all_sorted_by(self) -> None:
        assert self.cars_service_instance.all_sorted_by('model', SortOrder.ASC) == self.cars[1::-1]
        assert self.cars_service_instance.all_sorted_by('model', SortOrder.DESC) == self.cars

        assert self.cars_service_instance.all_sorted_by('price', SortOrder.ASC) == self.cars
        assert self.cars_service_instance.all_sorted_by('price', SortOrder.DESC) == self.cars[1::-1]

        assert self.cars_service_instance.all_sorted_by('color', SortOrder.ASC) == self.cars[1::-1]
        assert self.cars_service_instance.all_sorted_by('color', SortOrder.DESC) == self.cars

        assert self.cars_service_instance.all_sorted_by('mileage', SortOrder.ASC) == self.cars
        assert self.cars_service_instance.all_sorted_by('mileage', SortOrder.DESC) == self.cars[1::-1]

        assert self.cars_service_instance.all_sorted_by('components', SortOrder.ASC) == self.cars
        assert self.cars_service_instance.all_sorted_by('components', SortOrder.DESC) == self.cars[1::-1]

    def test_all_sorted_by_with_invalid_attr_name(self) -> None:
        with pytest.raises(ValueError) as e:
            self.cars_service_instance.all_sorted_by('fake_attr', SortOrder.DESC)
        assert e.value.args[0] == 'Invalid attribute name'


    def test__get_statistics_for_numeric_field(self) -> None:
        assert self.cars_service_instance._get_statistics_for_numeric_field(self.cars, 'price') == {
            "min": Decimal('100'),
            "max": Decimal('101'),
            "avg": Decimal('100.5')
        }
        assert self.cars_service_instance._get_statistics_for_numeric_field(self.cars, 'mileage') == {
            "min": 100,
            "max": 101,
            "avg": 100.5
        }

        with pytest.raises(ValueError) as e:
            self.cars_service_instance._get_statistics_for_numeric_field(self.cars, 'model')
        assert e.value.args[0]

    def test_get_statistics_for_numeric_field(self) -> None:
        assert self.cars_service_instance.get_statistics_for_numeric_fields(['mileage']) == {
            "mileage" : {
            "min": 100,
            "max": 101,
            "avg": 100.5
            }
        }

        assert self.cars_service_instance.get_statistics_for_numeric_fields(['mileage', 'price']) == {
            "mileage": {
                "min": 100,
                "max": 101,
                "avg": 100.5
            },
            "price": {
            "min": Decimal('100'),
            "max": Decimal('101'),
            "avg": Decimal('100.5')
            }
        }

    def test_with_mileage_gt(self) -> None:
        assert self.cars_service_instance.with_mileage_gt(100) == [self.cars[1]]

    def test_cars_color_map(self) -> None:
        assert self.cars_service_instance.cars_colors_map() == {
            Color.WHITE: [self.cars[0]],
            Color.BLACK: [self.cars[1]],
        }

    def test_models_with_most_expensive_cars(self) -> None:
        assert self.cars_service_instance.models_with_most_expensive_cars() == {
            'AUDI': [self.cars[1]],
            'BMW': [self.cars[0]]
        }

    def test_most_expensive_cars(self) -> None:
        assert self.cars_service_instance.most_expensive_cars() == [self.cars[1]]

    def test_cars_with_sorted_components(self) -> None:
        cars_with_many_components = [
        Car('BMW', Decimal('100'), Color.WHITE, 100, [Component('Radio'), Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/YzhkLmpwdhsJCTpeXwx7D0pRbkIRFHQcAQcpQhMWK1ceDj4eGRg3VV0IKFRHFDoeXVx5XUIWYUpRDn4JERRhHkYBPApSCg.jpg"),
        Car('AUDI', Decimal('101'), Color.BLACK, 101, [Component('DC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg")
        ]
        self.repo_mock.all_cars.return_value = cars_with_many_components

        assert self.cars_service_instance.cars_with_sorted_components()[0].components == [Component('AC'), Component('Radio')]

        self.repo_mock.all_cars.return_value = self.cars
    def test_components_with_cars_map(self) -> None:
        assert self.cars_service_instance.components_with_cars_map() == {
            Component('AC'): [self.cars[0]],
            Component('DC'): [self.cars[1]]
        }

    def test_cars_with_price_in_range_sorted_by(self) -> None:
        assert self.cars_service_instance.cars_with_price_in_range_sorted_by((Decimal('99'), Decimal('101')), SortOrder.ASC) == [
            self.cars[0], self.cars[1]
        ]

        assert self.cars_service_instance.cars_with_price_in_range_sorted_by((Decimal('99'), Decimal('101')), SortOrder.DESC) == [
            self.cars[1], self.cars[0]
        ]