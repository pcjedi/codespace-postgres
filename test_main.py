import os
import sqlalchemy as sa
from main import initdb


def test_initdb():
    root_engine = sa.create_engine("postgresql+psycopg2://postgres:postgres@" + os.getenv("POSTGRES_HOST"))
    engine = initdb(root_engine)
    with engine.begin():
        assert True
