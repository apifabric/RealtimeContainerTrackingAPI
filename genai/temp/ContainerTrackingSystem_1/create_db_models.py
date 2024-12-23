# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py

from sqlalchemy.dialects.sqlite import *


class Container(Base):\n    __tablename__ = 'container'\n    \n    id = Column(Integer, primary_key=True, autoincrement=True)\n    serial_number = Column(String)\n    description = Column(String)\n    creation_date = Column(DateTime)\n\n    """description: Table representing a container with its serial number and creation date."""


class Shipment(Base):\n    __tablename__ = 'shipment'\n    \n    id = Column(Integer, primary_key=True, autoincrement=True)\n    tracking_number = Column(String)\n    origin = Column(String)\n    destination = Column(String)\n    departure_date = Column(DateTime)\n    arrival_date = Column(DateTime)\n\n    """description: Table that stores the shipment details including tracking number, origin, and destination."""


class Location(Base):\n    __tablename__ = 'location'\n    \n    id = Column(Integer, primary_key=True, autoincrement=True)\n    name = Column(String)\n    address = Column(String)\n    type = Column(String)\n\n    """description: Represents a physical location, including name and address."""


class ContainerLog(Base):\n    __tablename__ = 'container_log'\n    \n    id = Column(Integer, primary_key=True, autoincrement=True)\n    container_id = Column(Integer, ForeignKey('container.id'))\n    location_id = Column(Integer, ForeignKey('location.id'))\n    timestamp = Column(DateTime)\n    status = Column(String)\n\n    """description: Logs the container's movement, tracking the location and status during transit."""


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    container_1 = Container(serial_number="CNTR001", description="Standard 20ft Container", creation_date=datetime(2023, 1, 15))
    shipment_1 = Shipment(tracking_number="TRCK001", origin="Port A", destination="Port B", departure_date=datetime(2023, 1, 15), arrival_date=datetime(2023, 1, 20))
    location_1 = Location(name="Port A", address="123 Ocean Rd", type="Port")
    container_log_1 = ContainerLog(container_id=1, location_id=1, timestamp=datetime(2023, 1, 15), status="Departed")
    
    
    
    session.add_all([container_1, shipment_1, location_1, container_log_1])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
