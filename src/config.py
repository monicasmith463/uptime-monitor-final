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

_db_url = os.getenv("DATABASE_URL")
if _db_url and _db_url.strip():
    DATABASE_URL = _db_url.replace("postgres://", "postgresql://", 1)
elif POSTGRES_SERVER and POSTGRES_USER and POSTGRES_DB:
    port_string = f":{POSTGRES_PORT}" if POSTGRES_PORT else ""
    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD or ''}"
        f"@{POSTGRES_SERVER}{port_string}/{POSTGRES_DB}"
    )
else:
    raise ValueError("database not configured")

_redis_url = os.getenv("REDIS_URL") or os.getenv("REDISCLOUD_URL")
if _redis_url:
    r = redis.from_url(_redis_url, decode_responses=True)
else:
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
