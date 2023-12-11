import pytest
from _decimal import Decimal

from app.models import Car, Color, Component
from app.repo import Operator


class TestMongoDBCarsRepo:
    """
    Test the all_cars method of the MongoDBCarsRepo class.

    Args:
        inserted_cars (list): List of cars expected to be inserted.
        mongo_repo (MongoDBCarsRepo): Instance of the MongoDBCarsRepo class.

    Raises:
        AssertionError: If the all_cars method does not return the expected inserted_cars.
    """
    bmw = Car('BMW M3', Decimal('100000'), Color.BLACK, 1, [Component('AC'), Component('ESP')],
              "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg")

    def test_all(self, inserted_cars, mongo_repo) -> None:
        """
        @param inserted_cars: The list of cars that were inserted into the repository.
        @param mongo_repo: The repository object that provides the 'all_cars' method.
        """
        assert mongo_repo.all_cars() == inserted_cars

    @pytest.mark.parametrize("operator, value, expected_value", [
        [Operator.EQ, 1, 2],
        [Operator.NE, 1, 8],
        [Operator.GT, 400_000, 1],
        [Operator.LT, 2, 2],
        [Operator.GE, 1, 10],
        [Operator.LE, 1, 2],
        ['FAKE_OPERATOR', 1, {"exception": TypeError, "error_msg": 'Invalid operator'}]
    ])
    def test_with_mileage(self, mongo_repo, operator, value, expected_value) -> None:
        """
        @param mongo_repo: The repository for querying mileage data.
        @param operator: The comparison operator used in the query.
        @param value: The value to compare against in the query.
        @param expected_value: The expected number of results from the query.
        """
        if type(expected_value) is int:
            assert len(mongo_repo.with_mileage(operator, value)) == expected_value
        else:
            with pytest.raises(TypeError) as e:
                mongo_repo.with_mileage(operator, value)
            assert e.value.args[0] == 'Invalid operator'

    @pytest.mark.parametrize("price_min, price_max, expected_value", [
        [Decimal('100000'), Decimal('110000'), 2],
        [Decimal('-1'), Decimal('-2'), {"exception": ValueError, "error_msg": "Price range cannot be negative"}],
        [Decimal('2'), Decimal('1'), {"exception": ValueError, "error_msg": "Invalid price range"}]

    ])
    def test_with_price(self, mongo_repo, price_min, price_max, expected_value) -> None:
        """
        @param mongo_repo: The MongoDB repository object.
        @param price_min: The minimum price value for the price range.
        @param price_max: The maximum price value for the price range.
        @param expected_value: The expected value for the test case.

        """
        if type(expected_value) is int:
            assert len(mongo_repo.with_price_between(price_min, price_max)) == expected_value
        else:
            with pytest.raises(expected_value['exception']) as e:
                mongo_repo.with_price_between(price_min, price_max)
            assert e.value.args[0] == expected_value['error_msg']
