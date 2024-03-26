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


class admins(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)


class adminmodel():
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def insert(self):
        with engine.connect() as connection:
            stmt = insert(admins).values(email=self.email, password=self.password)
            connection.execute(stmt)
            connection.commit()
