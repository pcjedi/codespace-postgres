import os
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


class Car(Base):
    __tablename__ = "Cars"

    Id = sa.Column(sa.Integer, primary_key=True)
    Name = sa.Column(sa.String)
    Price = sa.Column(sa.Integer)

    def __repr__(self):
        return f"Id:{self.Id},Name:{self.Name},Price:{self.Price}"


def create_user_n_database(name, pw, root_engine):
    with root_engine.begin() as sess:
        sess.execute("COMMIT")
        try:
            sess.execute(f"CREATE USER {name} WITH PASSWORD '{pw}'")
        except sa.exc.ProgrammingError as e:
            print(e)
        try:
            sess.execute(f"CREATE DATABASE {name}")
        except sa.exc.ProgrammingError as e:
            print(e)
            sess.execute("DROP DATABASE " + name)
            sess.execute(f"CREATE DATABASE {name}")
        sess.execute(f"GRANT ALL PRIVILEGES ON DATABASE {name} TO {name}")


def drop_database(name, root_engine):
    with root_engine.begin() as sess:
        sess.execute("COMMIT")
        try:
            sess.execute("DROP DATABASE " + name)
        except sa.exc.ProgrammingError as e:
            print(e)


def drop_user(name, root_engine):
    with root_engine.begin() as sess:
        try:
            sess.execute(f"REASSIGN OWNED BY {name} TO postgres")
        except sa.exc.ProgrammingError as e:
            print(e)
            return
        sess.execute("DROP OWNED BY " + name)
        sess.execute("DROP USER " + name)


def initdb(root_engine):
    create_user_n_database("dev", "dev", root_engine)
    engine = sa.create_engine("postgresql+psycopg2://dev:dev@" + os.getenv("POSTGRES_HOST") + "/dev")
    Base.metadata.create_all(bind=engine)
    return engine


allcars = [
    {"Price": 52642, "Name": "Audi", "Id": 1},
    {"Price": 57127, "Name": "Mercedes", "Id": 2},
    {"Price": 9000, "Name": "Skoda", "Id": 3},
    {"Price": 29000, "Name": "Volvo", "Id": 4},
    {"Price": 350000, "Name": "Bentley", "Id": 5},
    {"Price": 21000, "Name": "Citroen", "Id": 6},
    {"Price": 41400, "Name": "Hummer", "Id": 7},
    {"Price": 21600, "Name": "Volkswagen", "Id": 8},
]


def coreflow():
    root_engine = sa.create_engine(name_or_url="postgresql+psycopg2://postgres:postgres@" + os.getenv("POSTGRES_HOST"))
    engine = initdb(root_engine)
    with engine.begin() as conn:
        conn.execute(Base.metadata.tables["Cars"].insert(), allcars)
        print(len(list(conn.execute(Base.metadata.tables["Cars"].select()))), "items in db")
    cleanup(engine, root_engine)


def ormflow():
    root_engine = sa.create_engine(name_or_url="postgresql+psycopg2://postgres:postgres@" + os.getenv("POSTGRES_HOST"))
    engine = initdb(root_engine)
    ses = Session(engine)
    ses.add_all([Car(**car) for car in allcars])
    print(len(ses.query(Car).all()), "items in db")
    ses.close()


def cleanup(engine, root_engine):
    engine.dispose()
    drop_database("dev", root_engine)
    drop_user("dev", root_engine)


if __name__ == "__main__":
    coreflow()
    ormflow()
