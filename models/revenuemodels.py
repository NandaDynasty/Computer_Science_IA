from flask import Flask, jsonify
import mysql.connector
from sqlalchemy import create_engine, select, Float, update, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, VARCHAR, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER, insert
from datetime import datetime
from base import Base
from engine import engine


class monthlyrevenue(Base):
    __tablename__ = "monthlyrevenue"

    mr_id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String(100), nullable=False)
    year = Column(String(100), nullable=False)
    total_revenue = Column(Float, nullable=False)


class mrmodel():
    def __init__(self, month, year, total_revenue):
        self.month = month
        self.year = year
        self.total_revenue = total_revenue
    def update(self):
        with engine.connect() as connection:
            stmt = update(monthlyrevenue).where(
                and_(monthlyrevenue.month == self.month, monthlyrevenue.year == self.year)).values(
                total_revenue=self.total_revenue)
            connection.execute(stmt)
            connection.commit()
    def insert(self):
        with engine.connect() as connection:
            stmt = insert(monthlyrevenue).values(year=self.year, month=self.month, total_revenue=self.total_revenue)
            connection.execute(stmt)
            connection.commit()
