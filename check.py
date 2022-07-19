'''import pymysql
import pyodbc
import sqlalchemy as db
from sqlalchemy import create_engine
import pandas as pd
from flask import make_response
import json
from check import *
from constraints import *
from config import *
from flask_sqlalchemy import SQLAlchemy
print(111)
engine = db.create_engine("mysql://root:xx3721xx@39.103.183.155/user?charset=utf8")
connection = engine.connect()
metadata = db.MetaData()
user = db.Table('user_info', metadata, autoload=True, autoload_with=engine)
# Print the column names
print(user.columns.keys())
print(repr(metadata.tables['user_info']))

query = db.select([user])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet[:3])

db.select([user]).where(user.columns.role == 'User')
result=connection.execute(query)
resultset =result.fetchall()
print(resultset)

'''