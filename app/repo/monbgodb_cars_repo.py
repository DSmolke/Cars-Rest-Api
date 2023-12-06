from _decimal import Decimal
from dataclasses import dataclass

from app.models import Car
from app.repo import Operator
from app.repo.abc import CarsRepository

from pymongo import MongoClient


@dataclass
class MongoDBCarsRepo(CarsRepository):
    uri: str
    port: int

    def all_cars(self) -> [Car]:
        with MongoClient(self.uri, port=self.port) as client:
            db = client.db
            cars = db.cars

            return [Car.from_json_dict(car_data) for car_data in cars.find({})]



    def with_mileage(self, operator: Operator, value: int) -> [Car]:
        MAX_MILEAGE: Final = 6_000_000

        with MongoClient(self.uri, self.port) as client:
            db = client.db
            cars = db.cars

            match operator:
                case Operator.EQ:
                    return [Car.from_json_dict(car_data) for car_data in cars.find({"mileage": {"$eq": value}})]

                case Operator.NE:
                    return [Car.from_json_dict(car_data) for car_data in cars.find({"mileage": {"$ne": value}})]

                case Operator.GT:
                    return [Car.from_json_dict(car_data) for car_data in cars.find({"mileage": {"$gt": value}})]
                case Operator.LT:
                    return [Car.from_json_dict(car_data) for car_data in cars.find({"mileage": {"$lt": value}})]

                case Operator.GE:
                    return [Car.from_json_dict(car_data) for car_data in cars.find({"mileage": {"$gte": value}})]

                case Operator.LE:
                    return [Car.from_json_dict(car_data) for car_data in cars.find({"mileage": {"$lte": value}})]

                case _:
                    raise TypeError('Invalid operator')

    def with_price_between(self, price_min: Decimal, price_max: Decimal) -> [Car]:
        if price_min < 0 or price_max < 0:
            raise ValueError('Price range cannot be negative')
        if price_min > price_max:
            raise ValueError('Invalid price range')
        with MongoClient(self.uri, self.port) as client:
            db = client.db
            cars = db.cars
            result = [Car.from_json_dict(car_data) for car_data in cars.find({})]
            return [c for c in result if c.has_price_between(price_min, price_max)]