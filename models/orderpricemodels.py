from flask import Flask, jsonify
import mysql.connector
from sqlalchemy import create_engine, insert, select, bindparam, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, VARCHAR, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base
from engine import engine


class orderprice(Base):
    __tablename__ = "orderprice"

    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    total_price = Column(Float, nullable=False)

    orders = relationship('orders')


class opmodel():
    def __init__(self, order_id, total_price):
        self.order_id = order_id
        self.total_price = total_price

    def insert(self):
        with engine.connect() as connection:
            stmt = insert(orderprice).values(order_id=self.order_id, total_price=self.total_price)
            connection.execute(stmt)
            connection.commit()
