import sqlalchemy
import mysql.connector as sql
import pymysql
import os
import sys
from decouple import Config
from sqlalchemy import text
import pandas as pd
from sqlalchemy.exc import StatementError, ResourceClosedError

config = Config('.env')

my_UserName = config('DB_USERNAME')
my_Password = config('DB_PASSWORD')
my_Hostname = config('DB_HOSTNAME')
my_DatabaseName = config('DB_DATABASE')

db_connection_str = f"mysql+pymysql://{my_UserName}:{my_Password}@{my_Hostname}/{my_DatabaseName}"
engine = sqlalchemy.create_engine(db_connection_str)

class DatabaseConnection:
    _instance = None

    def __new__(cls, engine):
        if cls._instance is None:
            print("Creating a new database connection.")
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.engine = engine
            cls._instance.connect()
        return cls._instance

    def connect(self):
        try:
            self.connection = self.engine.connect()
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None
            sys.exit(1)

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_connection(self):
        try:
            # Testa se a conexão ainda está válida
            if self.connection is not None:
                self.connection.execute(text("SELECT 1"))
        except (StatementError, ResourceClosedError, AttributeError):
            print("Connection is closed. Reconnecting...")
            self.close()
            self.connect()

        if self.connection is None:
            self.connect()

        return self.connection


def my_read(sql, index_col=None, params_col=None):
    db_instance = DatabaseConnection(engine)
    nconnection = db_instance.get_connection()

    dataset = pd.read_sql(sql, con=nconnection, index_col=index_col, params=params_col)
    return dataset


def my_close():
    db_instance = DatabaseConnection(engine)
    nconnection = db_instance.close()

