from sqlalchemy import create_engine
from sqlalchemy import URL

from sqlalchemy import MetaData, Table

import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

db_driver = config['database']['drivername']
db_user = config['database']['username']
db_password = config['database']['password']
db_host = config['database']['host']
db_port = config['database'].getint('port')
db_name = config['database']['database']

print(db_driver, db_user, db_password, db_host, db_port, db_name)

metadata_obj = MetaData()

url_object = URL.create(
    drivername=db_driver,
    username=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_name
)

engine = create_engine(url_object)

table_core_invoice_items = Table('core_invoice_item', metadata_obj, autoload_with=engine)

