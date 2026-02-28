# Source - https://stackoverflow.com/a/41547163
# Posted by Will, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-18, License - CC BY-SA 4.0

# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv
import redis

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

if POSTGRES_PORT:
    port_string = f":{POSTGRES_PORT}"
else:
    port_string = ""  

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_SERVER}{port_string}/{POSTGRES_DB}"
)

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
