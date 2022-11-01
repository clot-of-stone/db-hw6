import json
import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
NAME_DB = os.getenv("NAME_DB")
DSN = f'postgresql://{LOGIN}:{PASSWORD}@localhost:5432/{NAME_DB}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()


def init_db(session):
    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)
        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
        session.commit()


def search_shop(publisher):
    results = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher).all()
    for s in results:
        print(f'Shop: {s.id}, {s.name}')


def search_publisher(name_id):
    for publisher in session.query(Publisher).all():
        if publisher.name == name_id:
            return print(publisher)
        elif name_id.isdigit() and int(name_id) == publisher.id:
            return publisher
    else:
        return "Ничего не найдено"


if __name__ == "__main__":
    init_db(session)
    publisher = input("Ведите имя издателя для поиска магазина: ")
    search_shop(publisher)
    name_id = input("Ведите имя или id издателя: ")
    print(search_publisher(name_id))
