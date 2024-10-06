import os

from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

JWT_TOKEN_LIFETIME = int(os.environ['JWT_TOKEN_LIFETIME'])
