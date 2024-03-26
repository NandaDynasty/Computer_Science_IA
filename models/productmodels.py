from flask import Flask, jsonify
import mysql.connector
from sqlalchemy import create_engine, insert, select, bindparam, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, VARCHAR, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base
from engine import engine


class products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    product_type = Column(String(100), nullable=False)
    product_image = Column(String(1000), nullable=False)
    product_details = Column(String(100000), nullable=False)
    price = Column(Float, nullable=False)


class productmodel():
    def __init__(self, product_name, product_type, product_image, price, details):
        self.product_name = product_name
        self.product_type = product_type
        self.product_image = product_image
        self.price = price
        self.product_details = details

    def insert(self):
        with engine.connect() as connection:
            stmt = insert(products).values(product_name=self.product_name, product_type=self.product_type, product_image=self.product_image , price=self.price, product_details=self.product_details)
            connection.execute(stmt)
            connection.commit()
