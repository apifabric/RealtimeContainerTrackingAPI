# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 23, 2024 15:52:22
# Database: sqlite:////tmp/tmp.5dcroQfXMC-01JFT3DMRJTMVQSYBQXEXTVSXF/ContainerTrackingSystem/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Container(SAFRSBaseX, Base):
    """
    description: Stores information about the containers being tracked.
    """
    __tablename__ = 'container'
    _s_collection_name = 'Container'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_number = Column(String, nullable=False)
    description = Column(String)
    weight = Column(Integer)
    origin = Column(String)
    destination = Column(String)
    shipment_date = Column(Date)
    arrival_date = Column(Date)

    # parent relationships (access parent)

    # child relationships (access children)
    ContainerTrackingList : Mapped[List["ContainerTracking"]] = relationship(back_populates="container")
    ShipmentList : Mapped[List["Shipment"]] = relationship(back_populates="container")



class Customer(SAFRSBaseX, Base):
    """
    description: Stores customer information.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone_number = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")



class Driver(SAFRSBaseX, Base):
    """
    description: Information about drivers handling the shipments.
    """
    __tablename__ = 'driver'
    _s_collection_name = 'Driver'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    license_number = Column(String)
    phone_number = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ContainerTrackingList : Mapped[List["ContainerTracking"]] = relationship(back_populates="driver")



class Location(SAFRSBaseX, Base):
    """
    description: Represents locations where containers can be tracked.
    """
    __tablename__ = 'location'
    _s_collection_name = 'Location'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    ContainerTrackingList : Mapped[List["ContainerTracking"]] = relationship(back_populates="current_location")
    RouteList : Mapped[List["Route"]] = relationship(foreign_keys='[Route.end_location_id]', back_populates="end_location")
    startRouteList : Mapped[List["Route"]] = relationship(foreign_keys='[Route.start_location_id]', back_populates="start_location")
    ShipmentList : Mapped[List["Shipment"]] = relationship(back_populates="location")



class Product(SAFRSBaseX, Base):
    """
    description: Information about products being shipped.
    """
    __tablename__ = 'product'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    weight = Column(Integer)
    price = Column(Integer)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderProductList : Mapped[List["OrderProduct"]] = relationship(back_populates="product")



class ContainerTracking(SAFRSBaseX, Base):
    """
    description: Tracks the current location and status of containers.
    """
    __tablename__ = 'container_tracking'
    _s_collection_name = 'ContainerTracking'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_id = Column(ForeignKey('container.id'), nullable=False)
    current_location_id = Column(ForeignKey('location.id'), nullable=False)
    driver_id = Column(ForeignKey('driver.id'))
    status = Column(String)
    last_update = Column(DateTime)

    # parent relationships (access parent)
    container : Mapped["Container"] = relationship(back_populates=("ContainerTrackingList"))
    current_location : Mapped["Location"] = relationship(back_populates=("ContainerTrackingList"))
    driver : Mapped["Driver"] = relationship(back_populates=("ContainerTrackingList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Stores order information related to a customer.
    """
    __tablename__ = 'order'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False)
    order_date = Column(Date)
    delivery_date = Column(Date)
    status = Column(String)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderProductList : Mapped[List["OrderProduct"]] = relationship(back_populates="order")



class Route(SAFRSBaseX, Base):
    """
    description: Stores information about the preferred container routes.
    """
    __tablename__ = 'route'
    _s_collection_name = 'Route'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_location_id = Column(ForeignKey('location.id'), nullable=False)
    end_location_id = Column(ForeignKey('location.id'), nullable=False)

    # parent relationships (access parent)
    end_location : Mapped["Location"] = relationship(foreign_keys='[Route.end_location_id]', back_populates=("RouteList"))
    start_location : Mapped["Location"] = relationship(foreign_keys='[Route.start_location_id]', back_populates=("startRouteList"))

    # child relationships (access children)



class Shipment(SAFRSBaseX, Base):
    """
    description: Represents a shipment event for a container.
    """
    __tablename__ = 'shipment'
    _s_collection_name = 'Shipment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_id = Column(ForeignKey('container.id'), nullable=False)
    location_id = Column(ForeignKey('location.id'), nullable=False)
    timestamp = Column(DateTime)
    status = Column(String)

    # parent relationships (access parent)
    container : Mapped["Container"] = relationship(back_populates=("ShipmentList"))
    location : Mapped["Location"] = relationship(back_populates=("ShipmentList"))

    # child relationships (access children)



class OrderProduct(SAFRSBaseX, Base):
    """
    description: Relationship between orders and products.
    """
    __tablename__ = 'order_product'
    _s_collection_name = 'OrderProduct'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderProductList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderProductList"))

    # child relationships (access children)
