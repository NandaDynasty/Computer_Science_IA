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


class prodstock(Base):
    __tablename__ = "products_stock"

    stock_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    current_stock = Column(Integer, nullable=False)
    minimum_stock = Column(Integer, nullable=False)


class productstockmodel():
    def __init__(self, name, current_stock, minimum_stock):
        self.product_name = name
        self.current_stock = current_stock
        self.minimum_stock = minimum_stock


    def update(self):
        with engine.connect() as connection:
            stmt = update(prodstock).where(prodstock.product_name == self.product_name).values(
                current_stock=self.current_stock,
                minimum_stock=self.minimum_stock)
            connection.execute(stmt)
            connection.commit()

    def insert(self):
        with engine.connect() as connection:
            stmt = insert(prodstock).values(product_name=self.product_name, current_stock=self.current_stock,
                                        minimum_stock=self.minimum_stock)
            connection.execute(stmt)
            connection.commit()