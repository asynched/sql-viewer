from os import environ
from dotenv import load_dotenv

load_dotenv()

DATABASE_FILENAME = environ.get("DATABASE_FILENAME")
