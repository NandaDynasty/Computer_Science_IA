from flask import Flask, jsonify
import mysql.connector
from sqlalchemy import create_engine, select, Numeric, update, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, VARCHAR, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER, insert
from datetime import datetime

from sqlalchemy.orm import relationship

from base import Base
from engine import engine


class stock(Base):
    __tablename__ = "stock"

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_name = Column(String(100), nullable=False)
    current_stock = Column(Integer, nullable=False)
    minimum_stock = Column(Integer, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)


class stockmodel():
    def __init__(self, name, current_stock, minimum_stock, price):
        self.ingredient_name = name
        self.current_stock = current_stock
        self.minimum_stock = minimum_stock
        self.price = price

    def update(self):
        with engine.connect() as connection:
            stmt = update(stock).where(stock.ingredient_name == self.ingredient_name).values(
                current_stock=self.current_stock,
                minimum_stock=self.minimum_stock,
                price=self.price)
            connection.execute(stmt)
            connection.commit()

    def insert(self):
        with engine.connect() as connection:
            stmt = insert(stock).values(ingredient_name=self.ingredient_name, current_stock=self.current_stock,
                                        minimum_stock=self.minimum_stock,
                                        price=self.price)
            connection.execute(stmt)
            connection.commit()
