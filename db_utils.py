from sqlalchemy import *
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
import config
from utils import *


Base = declarative_base()


class DataBase:

    def __init__(self, db_username, db_password, db_name):
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name

    def create_and_connect_database(self):
        '''
        Creates the Database if it doesn't exist and returns the Connection object to it
        :return: con(Connection): returns Connection object for the database in MySQL
        '''

        engine = create_engine(f"mysql+pymysql://{self.db_username}:{self.db_password}@localhost:3306/{self.db_name}",
                               echo=True)

        if not database_exists(engine.url):
            create_database(engine.url)

        con = engine.connect()

        return con, engine


    def create_table(self, engine):

        meta = MetaData()

        contracts = Table(
            'contracts', meta,
            Column('name', String(8), primary_key=True),
            Column('date', Date, primary_key=True),
            Column('price', Float),
        )


        meta.create_all(engine)

        return contracts


def generate_sql_query(contract_root, singular=False):

    contract_names = get_contract_depth(contract_root)

    db_object = DataBase(config.db_username, config.db_password, config.db_name)

    con, engine = db_object.create_and_connect_database()

    contracts = db_object.create_table(engine)
    if not singular:
        query = select([contracts]).where(contracts.c.name.in_(contract_names))
    else:
        query = select([contracts]).where(contracts.c.name == contract_root)

    return engine, query







if __name__ == "__main__":

    db_username = config.db_username
    db_password = config.db_password
    db_name = config.db_name

    db_object = DataBase(db_username, db_password, db_name)

    con, engine = db_object.create_and_connect_database()


    table = db_object.create_table(engine)




