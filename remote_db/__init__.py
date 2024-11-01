from sqlalchemy import *
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from config import settings

engine = create_engine(f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD.get_secret_value()}@{settings.DB_HOST}/{settings.DB_NAME}")
metadata = MetaData()
metadata.reflect(bind=engine)

Base = declarative_base()

class TurbineFarm(Base):
  __table__ = Table('turbine_farm', metadata, autoload=True)

# # Create a Session
Session = sessionmaker(bind=engine, autocommit=False)
def get_session():
    while True:
        try:
            session = Session()
            yield session
            session.commit()
            break
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()
