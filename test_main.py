import sqlalchemy as sa
from main import initdb


def test_initdb():
    root_engine = sa.create_engine("postgresql+psycopg2://postgres:postgres@postgres")
    engine = initdb(root_engine)
    with engine.begin():
        assert True
