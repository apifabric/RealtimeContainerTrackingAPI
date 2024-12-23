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


class Container(Base):
    """description: Stores information about the containers being tracked."""
    __tablename__ = 'container'
    id = Column(Integer, primary_key=True, autoincrement=True)
    container_number = Column(String, nullable=False)
    description = Column(String)
    weight = Column(Integer)
    origin = Column(String)
    destination = Column(String)
    shipment_date = Column(Date)
    arrival_date = Column(Date, nullable=True)


class Location(Base):
    """description: Represents locations where containers can be tracked."""
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)


class Shipment(Base):
    """description: Represents a shipment event for a container."""
    __tablename__ = 'shipment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(Integer, ForeignKey('container.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    timestamp = Column(DateTime)
    status = Column(String)


class Customer(Base):
    """description: Stores customer information."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone_number = Column(String)


class Order(Base):
    """description: Stores order information related to a customer."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    order_date = Column(Date)
    delivery_date = Column(Date, nullable=True)
    status = Column(String)


class Product(Base):
    """description: Information about products being shipped."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    weight = Column(Integer)
    price = Column(Integer)


class OrderProduct(Base):
    """description: Relationship between orders and products."""
    __tablename__ = 'order_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer)


class Route(Base):
    """description: Stores information about the preferred container routes."""
    __tablename__ = 'route'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    end_location_id = Column(Integer, ForeignKey('location.id'), nullable=False)


class Driver(Base):
    """description: Information about drivers handling the shipments."""
    __tablename__ = 'driver'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    license_number = Column(String)
    phone_number = Column(String)


class ContainerTracking(Base):
    """description: Tracks the current location and status of containers."""
    __tablename__ = 'container_tracking'
    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(Integer, ForeignKey('container.id'), nullable=False)
    current_location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('driver.id'))
    status = Column(String)
    last_update = Column(DateTime)


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    container1 = Container(container_number="CNT123", description="Container 1", weight=3000, origin="Port A", destination="Port B", shipment_date=date(2023, 10, 1), arrival_date=None)
    location1 = Location(name="Warehouse A", address="123 Main St, City A", country="Country X", latitude=47.6205, longitude=-122.3493)
    shipment1 = Shipment(container_id=1, location_id=1, timestamp=date(2023, 10, 1), status="In-transit")
    customer1 = Customer(name="John Doe", email="john@example.com", phone_number="123-456-7890")
    order1 = Order(customer_id=1, order_date=date(2023, 10, 5), delivery_date=None, status="Pending")
    product1 = Product(name="Gadget", description="High-tech gadget", weight=200, price=99)
    orderproduct1 = OrderProduct(order_id=1, product_id=1, quantity=10)
    route1 = Route(name="Route A", description="Fast route", start_location_id=1, end_location_id=2)
    driver1 = Driver(name="Alice Smith", license_number="D1234567", phone_number="987-654-3210")
    containertracking1 = ContainerTracking(container_id=1, current_location_id=1, driver_id=1, status="In-transit", last_update=date(2023, 10, 1))
    
    
    
    session.add_all([container1, location1, shipment1, customer1, order1, product1, orderproduct1, route1, driver1, containertracking1])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
