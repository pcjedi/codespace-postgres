import sqlalchemy as sa
from main import initdb


def test_initdb():
    root_engine = sa.create_engine(name_or_url="postgresql+psycopg2://postgres:postgres@localhost")
    engine = initdb(root_engine)
    with engine.begin():
        assert True
