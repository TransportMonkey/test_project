# config.py
import os

ENV = "development"
DEBUG = False
# SQLALCHEMY_DATABASE_URI = f'sqlite:///../{os.path.join("db", "test.db")}'
SQLALCHEMY_DATABASE_URI = f'mysql://root:lzy110101@localhost:3306/prod'
