from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'sqlite:////srv/sites/trello_workon/trello_workon/trello_workon.db',
    convert_unicode=True,
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import (
        user,
        case,
    )
    Base.metadata.create_all(bind=engine)


def reset_db():
    from models import (
        user,
        case,
    )
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
