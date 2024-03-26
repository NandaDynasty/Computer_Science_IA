from flask import Flask, jsonify
import mysql.connector
from sqlalchemy import create_engine, select, Float, update, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, VARCHAR, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER, insert
from datetime import datetime
from base import Base
from engine import engine


class morerevenue(Base):
    __tablename__ = "morerevenue"

    mr_id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String(100), nullable=False)
    year = Column(String(100), nullable=False)
    revenue = Column(Float, nullable=False)

class moremodel():
    def __init__(self, month, year, revenue):
        self.month = month
        self.year = year
        self.revenue = revenue
    def update(self):
        with engine.connect() as connection:
            stmt = update(morerevenue).where(
                and_(morerevenue.month == self.month, morerevenue.year == self.year)).values(
                revenue=self.revenue)
            connection.execute(stmt)
            connection.commit()
    def insert(self):
        with engine.connect() as connection:
            stmt = insert(morerevenue).values(year=self.year, month=self.month, revenue=self.revenue)
            connection.execute(stmt)
            connection.commit()
