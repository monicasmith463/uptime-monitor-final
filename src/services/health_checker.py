import json
import time
import requests
from src.config import r
import schedule

from src.database import SessionLocal
from src.models import Site, HealthCheck


def health_check(url: str, timeout: int = 10):
    request_url = url if url.startswith(("http://", "https://")) else "https://" + url
    try:
        start = time.time()
        response = requests.get(request_url, timeout=timeout, verify=False)
        response_time = time.time() - start
        status_code = response.status_code
        return {"site": url, "response_time": response_time, "status_code": status_code, "error": None}
    except Exception as e:
        error = str(e)
        return { "site": url, "response_time": None, "status_code": None, "error": error }


def perform_batch_health_check():
    db = SessionLocal()
    try:
        sites = db.query(Site).all()
        for site in sites:
            result = health_check(site.url)

        # write to the queue
            r.publish("latency", json.dumps(result))

    finally:
        db.close()

if __name__ == "__main__":
    schedule.every(15).seconds.do(perform_batch_health_check)
    while True:
        schedule.run_pending()
        time.sleep(1)