import os
import sys
from datetime import datetime

from dotenv import load_dotenv


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from data_insert.roles_insert import roles_insert
from data_insert.users_insert import users_load


load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

connection_params = {"database": DB_NAME, "user": DB_USER, "password": DB_PASS, "host": DB_HOST, "port": DB_PORT}

if __name__ == "__main__":
    start = datetime.now()
    roles_insert(connection_params)
    users_load(connection_params)
    print(f"Данные добавлены выполнена за: {datetime.now() - start}")
