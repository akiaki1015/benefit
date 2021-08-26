import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

DB = {
    'host': os.environ.get("DB_HOST"),
    'name': os.environ.get("DB_NAME"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD"),
    'port': os.environ.get("DB_PORT"),
}

BENEFIT = {
    'user': os.environ.get("BENEFIT_USER"),
    'password': os.environ.get("BENEFIT_PASSWORD"),
}
