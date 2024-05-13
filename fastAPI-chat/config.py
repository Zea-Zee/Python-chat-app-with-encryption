from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

DB_USER_TEST = os.environ.get('DB_USER')
DB_PASS_TEST = os.environ.get('DB_PASS')
DB_HOST_TEST = os.environ.get('DB_HOST')
DB_PORT_TEST = os.environ.get('DB_PORT')
DB_NAME_TEST = os.environ.get('DB_NAME')

JWT_SECRET = str(os.environ.get('JMTSecret'))
USER_MANAGER_SECRET = os.environ.get('UserManagerSecret')

SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
