import os

import dotenv
from dotenv import load_dotenv

dotenv_path = dotenv.find_dotenv(".env", usecwd=True)
load_dotenv(dotenv_path=dotenv_path)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

