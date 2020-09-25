import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class DBSession:
    _engine = None
    _dsn = None

    @classmethod
    def initdsn(cls, dsn):
        cls._dsn = dsn

    @classmethod
    def getsession(cls):
        """ This is a class method. It will create the alchemy engine if it does not exist.
            Will return a new session object to be used to create a query
        """

        if cls._dsn is None:
            return None

        if cls._engine is None:
            cls._engine = sqlalchemy.create_engine("postgresql+psycopg2://%s" % cls._dsn, echo=False, pool_recycle=60)
            cls._Session = sessionmaker(bind=cls._engine)

        return cls._Session()

@contextmanager
def session_scope():
    session = DBSession.getsession()
    try:
        yield session
    finally:
        if session is not None:
            session.close()