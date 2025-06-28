# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

db = SQLAlchemy()

db2 = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1234',
    database='lab3'
)
