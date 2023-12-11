import pytest
from decimal import Decimal

from app.models import Car, Color, Component

from app.repo import LocalCarsRepository
from app.repo.common_objects import Operator


class TestLocalCarsRepository:
    """
    Class TestLocalCarsRepository

    This class is used to test the functionality of the LocalCarsRepository class.

    Attributes:
        cars_collection (list[Car]): A collection of Car objects.
        local_cars_repository_instance (LocalCarsRepository): An instance of the LocalCarsRepository class.

    Methods:
        test_all_cars: This method tests the "all_cars" method of the LocalCarsRepository class.
        test_with_mileage: This method tests the "with_mileage" method of the LocalCarsRepository class.
        test_with_price_between: This method tests the "with_price_between" method of the LocalCarsRepository class.
    """
    cars_collection: [Car] = [
        Car('BMW', Decimal('100'), Color.WHITE, 100, [Component('AC')],
            "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg"),
        Car('AUDI', Decimal('101'), Color.WHITE, 101, [Component('AC')],
            "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_c1UuDL1pc55A.jpg")]

    local_cars_repository_instance = LocalCarsRepository(cars_collection)

    def test_all_cars(self) -> None:
        """
        Test all cars method.

        @return: None
        """
        assert self.local_cars_repository_instance.all_cars() == self.cars_collection

    @pytest.mark.parametrize("operator, value, expected_value", [
        [Operator.EQ, 100, [cars_collection[0]]],
        [Operator.NE, 100, [cars_collection[1]]],
        [Operator.GT, 100, [cars_collection[1]]],
        [Operator.LT, 101, [cars_collection[0]]],
        [Operator.GE, 100, cars_collection],
        [Operator.LE, 101, cars_collection],
        ['FAKE_OPERATOR', 100, {"exception": TypeError, "error_msg": 'Invalid operator'}]
    ])
    def test_with_mileage(self, operator, value, expected_value) -> None:
        """
        @param operator: The operator to use for filtering the cars based on their mileage. Should be an instance of the Operator enum.
        @param value: The value to compare the mileage against.
        @param expected_value: The expected result of the filtering operation.
        """
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
        (Decimal('-1'), Decimal('100'), {"exception": ValueError, "error_msg": 'Price range cannot be negative'})
    ])
    def test_with_price_between(self, price_min, price_max, expected_value) -> None:
        """
        @param price_min: The minimum price for filtering cars
        @param price_max: The maximum price for filtering cars
        @param expected_value: The expected result after filtering cars based on price range

        This method is used to test the "with_price_between" method of the local_cars_repository_instance. It takes in the minimum and maximum price values, as well as the expected result after
        * filtering cars based on the price range. The method uses pytest's "parametrize" decorator to specify multiple test cases.

        Example Usage:
        test_with_price_between(Decimal('100.00'), Decimal('101.00'), cars_collection)

        Parameters:
        - price_min (Decimal): The minimum price for filtering cars
        - price_max (Decimal): The maximum price for filtering cars
        - expected_value (list or dict): The expected result after filtering cars based on price range. If it's a list, it is compared directly with the result of the "with_price_between" method
        *. If it's a dictionary, it contains the expected exception type and error message, which are validated using pytest.raises.

        Example Test Cases:
        - Test case 1: Filtering cars with a price range of $100.00 to $101.00 should return the "cars_collection" list.
        - Test case 2: Filtering cars with a price range of $99.99 to $101.01 should return the "cars_collection" list.
        - Test case 3: Filtering cars with a price range of $100.00 to $100.00 should return a list containing only the first car from the "cars_collection".
        - Test case 4: Filtering cars with a negative price range should raise a ValueError exception with the error message 'Price range cannot be negative'.
        """
        if isinstance(expected_value, list):
            assert self.local_cars_repository_instance.with_price_between(price_min, price_max) == expected_value
        else:
            with pytest.raises(expected_value['exception']) as e:
                self.local_cars_repository_instance.with_price_between(price_min, price_max)
            assert e.value.args[0] == expected_value['error_msg']
