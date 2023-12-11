import mock
from decimal import Decimal

import pytest

from app.models import Car, Color, Component
from app.service import CarsService
from app.service.common_objects import SortOrder


class TestCarsService:
    """
    The TestCarsService class is a test suite for the CarsService class. It contains various test methods that test the functionality of the CarsService class.

    Attributes:
        cars (list): A list of Car instances used for testing.
        repo_mock (mock.Mock): A mock object to simulate a repository.
        cars_service_instance (CarsService): An instance of the CarsService class used for testing.

    Methods:
        test_all_cars() -> None:
            This method tests the 'all_cars' method of the CarsService class. It asserts that the 'all_cars' method returns the expected result.

        test_all_sorted_by() -> None:
            This method tests the 'all_sorted_by' method of the CarsService class. It asserts that the 'all_sorted_by' method returns the expected result for different attributes and sort
    * orders.

        test_all_sorted_by_with_invalid_attr_name() -> None:
            This method tests the 'all_sorted_by' method of the CarsService class when an invalid attribute name is provided. It asserts that a ValueError is raised with the expected error
    * message.

        test__get_statistics_for_numeric_field() -> None:
            This method tests the '_get_statistics_for_numeric_field' method of the CarsService class. It asserts that the '_get_statistics_for_numeric_field' method returns the expected
    * result for different numeric fields.

        test_get_statistics_for_numeric_field() -> None:
            This method tests the 'get_statistics_for_numeric_fields' method of the CarsService class. It asserts that the 'get_statistics_for_numeric_fields' method returns the expected
    * result for different numeric fields.

        test_with_mileage_gt() -> None:
            This method tests the 'with_mileage_gt' method of the CarsService class. It asserts that the 'with_mileage_gt' method returns the expected result for a given mileage.

        test_cars_color_map() -> None:
            This method tests the 'cars_colors_map' method of the CarsService class. It asserts that the 'cars_colors_map' method returns the expected result.

        test_models_with_most_expensive_cars() -> None:
            This method tests the 'models_with_most_expensive_cars' method of the CarsService class. It asserts that the 'models_with_most_expensive_cars' method returns the expected result
    *.

        test_most_expensive_cars() -> None:
            This method tests the 'most_expensive_cars' method of the CarsService class. It asserts that the 'most_expensive_cars' method returns the expected result.

        test_cars_with_sorted_components() -> None:
            This method tests the 'cars_with_sorted_components' method of the CarsService class. It asserts that the 'cars_with_sorted_components' method returns the expected result.

        test_components_with_cars_map() -> None:
            This method tests the 'components_with_cars_map' method of the CarsService class. It asserts that the '"""
    cars = [
        Car('BMW', Decimal('100'), Color.WHITE, 100, [Component('AC')],
            "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg"),
        Car('AUDI', Decimal('101'), Color.BLACK, 101, [Component('DC')],
            "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_c1UuDL1pc55A.jpg")
    ]
    repo_mock = mock.Mock(name='repo_mock')
    repo_mock.all_cars.return_value = cars
    repo_mock.with_mileage.return_value = [cars[1]]
    repo_mock.with_price_between.return_value = cars

    cars_service_instance = CarsService(repo_mock)

    def test_all_cars(self) -> None:
        """
        Test all cars from the cars service instance.
        """
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
        """
        Tests the behavior of the `all_sorted_by` method with an invalid attribute name.
        """
        with pytest.raises(ValueError) as e:
            self.cars_service_instance.all_sorted_by('fake_attr', SortOrder.DESC)
        assert e.value.args[0] == 'Invalid attribute name'

    def test__get_statistics_for_numeric_field(self) -> None:
        """
        Test the _get_statistics_for_numeric_field method of the CarsService class.
        This method tests the functionality of calculating statistics for a numeric field in a cars dataset.

        """
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
        """
        Test method for the `get_statistics_for_numeric_fields` function of the `cars_service_instance` object.

        It checks the correctness of the returned statistics given a list of numeric fields.

        Example usage:
            test_get_statistics_for_numeric_field()
        """
        assert self.cars_service_instance.get_statistics_for_numeric_fields(['mileage']) == {
            "mileage": {
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
        """
        Test method for the 'with_mileage_gt' function of the 'cars_service_instance' object.

        This method tests if the 'with_mileage_gt' function of the 'cars_service_instance' object
        correctly returns a list of cars with mileage greater than the provided value.
        """
        assert self.cars_service_instance.with_mileage_gt(100) == [self.cars[1]]

    def test_cars_color_map(self) -> None:
        """
        Test the cars color map generated by the cars_service_instance.
        """
        assert self.cars_service_instance.cars_colors_map() == {
            Color.WHITE: [self.cars[0]],
            Color.BLACK: [self.cars[1]],
        }

    def test_models_with_most_expensive_cars(self) -> None:
        """
        @test_models_with_most_expensive_cars:

        This method tests the functionality of the 'models_with_most_expensive_cars' method in the 'cars_service_instance'. It asserts that the expected output is equal to the provided dictionary
        *.
        """
        assert self.cars_service_instance.models_with_most_expensive_cars() == {
            'AUDI': [self.cars[1]],
            'BMW': [self.cars[0]]
        }

    def test_most_expensive_cars(self) -> None:
        """
        Test the most_expensive_cars method of the cars service.
        @raise AssertionError: If the result of most_expensive_cars() does not match the expected value.

        Example:
            >>> self.cars = ["car1", "car2", "car3"]
            >>> self.cars_service_instance.most_expensive_cars() == ["car2"]
        """
        assert self.cars_service_instance.most_expensive_cars() == [self.cars[1]]

    def test_cars_with_sorted_components(self) -> None:
        """
        @test_cars_with_sorted_components:

        This method tests the functionality of the 'cars_with_sorted_components' method in the CarsService class. It checks whether the method returns a list of cars with their components sorted
        * in a specific order.

        """
        cars_with_many_components = [
            Car('BMW', Decimal('100'), Color.WHITE, 100, [Component('Radio'), Component('AC')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/YzhkLmpwdhsJCTpeXwx7D0pRbkIRFHQcAQcpQhMWK1ceDj4eGRg3VV0IKFRHFDoeXVx5XUIWYUpRDn4JERRhHkYBPApSCg.jpg"),
            Car('AUDI', Decimal('101'), Color.BLACK, 101, [Component('DC')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg")
        ]
        self.repo_mock.all_cars.return_value = cars_with_many_components

        assert self.cars_service_instance.cars_with_sorted_components()[0].components == [Component('AC'),
                                                                                          Component('Radio')]

        self.repo_mock.all_cars.return_value = self.cars

    def test_components_with_cars_map(self) -> None:
        """
        Test the `components_with_cars_map` method of the `cars_service_instance`.
        """
        assert self.cars_service_instance.components_with_cars_map() == {
            Component('AC'): [self.cars[0]],
            Component('DC'): [self.cars[1]]
        }

    def test_cars_with_price_in_range_sorted_by(self) -> None:
        """
        This method is used to test the functionality of the `cars_with_price_in_range_sorted_by` method in the `cars_service_instance` object. It asserts whether the returned list of cars with
        * prices in the specified range is correctly sorted based on the given sort order.

        Parameters:
        - `self`: the current instance of the test class.

        Example usage:
            test_instance = TestClass()
            test_instance.test_cars_with_price_in_range_sorted_by()

        Note: This method assumes the existence of the `cars_service_instance` and `cars` attributes in the test class, and the `SortOrder` enum for specifying the sort order.
        """
        assert self.cars_service_instance.cars_with_price_in_range_sorted_by((Decimal('99'), Decimal('101')),
                                                                             SortOrder.ASC) == [
                   self.cars[0], self.cars[1]
               ]

        assert self.cars_service_instance.cars_with_price_in_range_sorted_by((Decimal('99'), Decimal('101')),
                                                                             SortOrder.DESC) == [
                   self.cars[1], self.cars[0]
               ]
