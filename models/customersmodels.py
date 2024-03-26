from flask import Flask, jsonify
import mysql.connector
from sqlalchemy import create_engine, select, update, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, VARCHAR, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER, insert
from datetime import datetime
from base import Base
from engine import engine


class customers(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    address = Column(String(500), nullable=False)
    phone_number = Column(VARCHAR(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)


class customersmodel():
    def __init__(self, first_name, last_name, address, number, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = number
        self.email = email
        self.password = password

    def insert(self):
        with engine.connect() as connection:
            stmt = insert(customers).values(first_name=self.first_name,
                                            last_name=self.last_name, address=self.address,
                                            phone_number=self.phone_number, email=self.email,
                                            password=self.password)
            connection.execute(stmt)
            connection.commit()


class updatedcustomer():
    def __init__(self, og_email, first_name, last_name, address, number, email, password):
        self.original = og_email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.number = number
        self.email = email
        self.password = password

    def update(self):
        with engine.connect() as connection:
            stmt = select(customers.customer_id).where(customers.email == self.original)
            row = connection.execute(stmt).fetchone()
            customer_id = row.customer_id
            stmt = update(customers).where(customers.customer_id == customer_id).values(first_name=self.first_name,
                                                                                        last_name=self.last_name,
                                                                                        address=self.address,
                                                                                        phone_number=self.number,
                                                                                        email=self.email,
                                                                                        password=self.password)
            connection.execute(stmt)
            connection.commit()
