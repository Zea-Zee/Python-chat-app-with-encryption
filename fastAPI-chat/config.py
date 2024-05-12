from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

JWT_SECRET = str(os.environ.get('JMTSecret'))
USER_MANAGER_SECRET = os.environ.get('UserManagerSecret')
