import configparser

from maria_db import MariaDb

config = configparser.ConfigParser()
config.read('db_config.ini')

# mariadb
db = MariaDb((config['mariadb']))


db.get_schema()
