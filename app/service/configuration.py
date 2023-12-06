from app.service.cars_service import CarsService
from app.repo.configuration import cars_repo, mongo_cars_repo


# Local repository variant
# cars_service_instance = CarsService(cars_repo)

# MongoDB repository variant
cars_service_instance = CarsService(mongo_cars_repo)
