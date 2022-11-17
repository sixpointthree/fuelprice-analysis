from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_NAME = 'fuelprices.db'

engine = create_engine(f'sqlite:///{DB_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

# create table prices with timestamp, price, station_id
class Prices(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    station_id = Column(Integer, ForeignKey('stations.id'))
    price_diesel = Column(Float)
    price_e5 = Column(Float)
    price_e10 = Column(Float)

# create table stations with id, name, brand, street, place, lat, lng
class Stations(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    name = Column(String)
    brand = Column(String)
    street = Column(String)
    place = Column(String)
    lat = Column(Integer)
    lng = Column(Integer)

Base.metadata.create_all(engine)
