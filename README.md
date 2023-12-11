# Cars REST API

Cars data providing API

## Getting Started

Here is a brief demo of project set up and functionalities
#### Registration
https://github.com/DSmolke/Samochody-01/assets/106284705/a120a530-0769-4496-b8c9-6f460afb45de

#### Authentication
https://github.com/DSmolke/Samochody-01/assets/106284705/f1855abc-032b-441a-ada4-3997500352db

#### Authorization and use cases
https://github.com/DSmolke/Samochody-01/assets/106284705/63868f1b-66a1-417e-9600-0c5e11785b75

#### Authorization troubleshooting
https://github.com/DSmolke/Samochody-01/assets/106284705/51f5e0ff-d536-4be5-9815-5903e0e73afa

## Prerequisites

To run a tests or app itself you need to install:
- python 3.11.0
- node v20.3.1
- docker engine
- pipenv
- git
- some IDE (I prefer Jetbrains solutions)

Make sure all ports placed in docker-compose.yml file aren't allocated by any other container.
List goes here: 3307, 3308, 27017, 8000, 3000, 80

## Installing

#### 1. Create docker containers
Position your cmd in project folder and run docker-compose
```
docker-compose up -d --build
```

#### 2. Run tests
Once your containers are up and running it's good time for tests. Once they'll be done, cars will be added to database for demo purposes.
```
pipenv install
pipenv run pytest
```

#### 3. Migration using alembic
Now it's time for migration. 'users' table will be created. We are almost ready for demo...
```
cd migrations/mysql
pipenv run alembic upgrade head
```
after that, come back to main directory:
```
cd ../..
```

#### 4. Start React ui
Last thing to do is start React app responsible for ui of the project. It's simple:
```
cd ui
npm install
npm start
```

Demo is ready!
Create an account, veryfi it on your email, and start using demo!

## Running the tests

Having containers ready 
```
docker-compose up -d --build
```
run
```
pipenv install
pipenv run pytest
```
(if only want to see tests results -> 1:15)
https://github.com/DSmolke/Cars-Rest-Api/assets/106284705/d8543412-c3e7-477a-8170-192c698a969d


## Tests specification
Development was done in TDD tone, all tests are made exclusively using pytest.

# Stack:
- Python (pytest, mock, werkzeug, python-dotenv, pyjwt)
- Flask (flask-restful, flask-mail, flask-cors)
- JS (axios, bootstrap)
- MongoDB (pymongo)
- MySQL (flask-sqlalchemy, alembic)
- React (hooks)
- Docker
- AWS
- Postman


