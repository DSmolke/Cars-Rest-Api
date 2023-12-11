from pymongo import MongoClient


from app.models import Car, Color, Component, Decimal



def upgrade(uri: str, port: int):
    with MongoClient(uri, port) as client:
        db = client.db
        cars = db.cars

        cars_entities = [
            Car('BMW M3', Decimal('100000'), Color.BLACK, 1, [Component('AC'), Component('ESP')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg"),
            Car('AUDI Q3', Decimal('110000'), Color.ORANGE, 1, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_c1UuDL1pc55A.jpg"),
            Car('MERCEDES E-CLASS', Decimal('120000'), Color.GREEN, 60_000, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_QMRgexEMCyEo.jpg"),
            Car('MAZDA 626', Decimal('7000'), Color.GREEN, 400_000, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_312941CRiY5i1V.jpg"),
            Car('FORD MONDEO', Decimal('15000'), Color.WHITE, 350_000, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_FuO8ylZBTpqW.jpg"),
            Car('FIAT 500', Decimal('45000'), Color.RED, 30_998, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_it8l7VC8BRVP.jpg"),
            Car('TOYOTA YARIS', Decimal('65000'), Color.WHITE, 40_560, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_RUvdJJ5OCqKO.jpg"),
            Car('IVECO DAILY', Decimal('78000'), Color.WHITE, 700_000, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_qbSmQi6OldHx.jpg"),
            Car('FSO POLONEZ', Decimal('3000'), Color.RED, 124_000, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_pcT71XtB7G7a.jpg"),
            Car('AUDI RS8', Decimal('850000'), Color.BLACK, 5_800, [Component('AC')], "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_314251K6G3nd4G.jpg"),
]

        cars.insert_many([car.to_dict() for car in cars_entities])


def downgrade(uri: str, port: int):
    with MongoClient(uri, port) as client:
        db = client.db
        cars = db.cars

        cars.delete_many({})

def upgrade2(uri, port):
    with MongoClient(uri, port) as client:
        db = client.db
        cars = db.cars

        cars.delete_many({})

        cars_entities2 = [
            Car('BMW M3', Decimal('100000'), Color.BLACK, 1, [Component('ESP'), Component('AC'), Component('4x4')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/80e1378e2cf8c496b6d0e63d3a913fcd.jpg"),
            Car('AUDI Q3', Decimal('110000'), Color.ORANGE, 1, [Component('AC'), Component('USB')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_c1UuDL1pc55A.jpg"),
            Car('MERCEDES E-CLASS', Decimal('120000'), Color.SILVER, 60_000, [Component('AC'),Component('AC'), Component('ESP'), Component('4x4'), Component('Ekran dotykowy')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_QMRgexEMCyEo.jpg"),
            Car('MAZDA 626', Decimal('7000'), Color.BLUE, 400_000, [Component('AC')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_312941CRiY5i1V.jpg"),
            Car('FORD MONDEO', Decimal('15000'), Color.SILVER, 350_000, [Component('AC'), Component('Zmiana biegów w kierownicy')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_FuO8ylZBTpqW.jpg"),
            Car('FIAT 500', Decimal('45000'), Color.RED, 30_998, [Component('AC')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_it8l7VC8BRVP.jpg"),
            Car('TOYOTA YARIS', Decimal('65000'), Color.RED, 40_560, [Component('Start-Stop'), Component('AC')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_RUvdJJ5OCqKO.jpg"),
            Car('IVECO DAILY', Decimal('78000'), Color.SILVER, 700_000, [Component('AC')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_qbSmQi6OldHx.jpg"),
            Car('FSO POLONEZ', Decimal('3000'), Color.ORANGE, 124_000, [Component('Szyby na korbkę'), Component('Skrzynia manualna')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_pcT71XtB7G7a.jpg"),
            Car('AUDI RS8', Decimal('850000'), Color.RED, 5_800, [Component('ESP'), Component('AC'),  Component('4x4'), Component('Zawieszenie sportowe')],
                "https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/oie_314251K6G3nd4G.jpg"),
        ]

        cars.insert_many([car.to_dict() for car in cars_entities2])
