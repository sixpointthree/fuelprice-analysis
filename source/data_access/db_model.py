from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_NAME = 'data/fuelprices.db'
PRICES_TABLE_NAME = 'prices'
STATIONS_TABLE_NAME = 'stations'

engine = create_engine(f'sqlite:///{DB_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

# create table prices with timestamp, price, station_id
class Prices(Base):
    __tablename__ = PRICES_TABLE_NAME
    timestamp = Column(Integer, primary_key=True)
    station_uuid = Column(String(length=36), ForeignKey('stations.uuid'), primary_key=True)
    price_diesel = Column(Float(precision=3))
    price_e5 = Column(Float(precision=3))
    price_e10 = Column(Float(precision=3))

# create table stations with id, name, brand, street, place, lat, lng
class Stations(Base):
    __tablename__ = STATIONS_TABLE_NAME
    uuid = Column(String(length=36), primary_key=True)
    name = Column(String)
    brand = Column(String(length=30))
    street = Column(String)
    place = Column(String)
    lat = Column(Float(precision=5))
    lon = Column(Float(precision=5))


#create db path recursively
def create_db_path():
    path = os.path.dirname(DB_NAME)
    if not os.path.exists(path):
        os.makedirs(path)

def remove_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f'Removed db {DB_NAME}')

def create_db():
    create_db_path()
    Base.metadata.create_all(engine)


create_db()
