# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:47:27 2024

@author: Shubham Singhal
"""

#!pip install SQLAlchemy
#!pip install sqlalchemy-orm
#!pip install sqlalchemy-repr
# setup_db.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLite database connection
engine = create_engine('sqlite:///bikes.db')
Base = declarative_base()

# Define a Bike model for the database
class Bike(Base):
    __tablename__ = 'bikes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
    month = Column(Integer)
    yeardiff = Column(Float)
    cc = Column(String)
    company = Column(String)
    model = Column(String)
    predicted_price = Column(Float)

# Create the table
Base.metadata.create_all(engine)

print("Database and table created successfully!")
