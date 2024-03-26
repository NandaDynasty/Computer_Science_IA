from flask import Flask, jsonify
import mysql.connector
from sqlalchemy import create_engine, insert, select, bindparam, Float, Date, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, VARCHAR, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base
from engine import engine


class orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(20), default="Pending", nullable=False)

    products = relationship('products')
    customers = relationship('customers')


class ordermodel():
    def __init__(self, order_id, product_id, customer_id, quantity, date):
        self.order_id = order_id
        self.product_id = product_id
        self.customer_id = customer_id
        self.quantity = quantity
        self.date = date

    def insert(self):
        with engine.connect() as connection:
            stmt = insert(orders).values(order_id=self.order_id, product_id=self.product_id,
                                         customer_id=self.customer_id, quantity=self.quantity,
                                         date=self.date)
            connection.execute(stmt)
            connection.commit()

class order_status():
    def __init__(self, id):
        self.order_id = id

    def update(self):
        with engine.connect() as connection:
            stmt = update(orders).where(orders.order_id == self.order_id).values(status="Done")
            connection.execute(stmt)
            connection.commit()
