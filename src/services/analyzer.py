import json

from src.config import r
from src.database import SessionLocal
from src.models import HealthCheck, Site


def analyze_health_check(payload):
    db = SessionLocal()
    try:
        url = payload["site"]
        site = db.query(Site).filter(Site.url == url).first()
        if not site:
            site = Site(url=url)
            db.add(site)
            db.flush()
        health_check = HealthCheck(
            site_id=site.id,
            response_time=payload.get("response_time"),
            status_code=payload.get("status_code"),
            error=payload.get("error"),
        )
        db.add(health_check)
        db.commit()
    except Exception as e:
        print("health check analysis has failed for URL:", url )
    finally:
        db.close()
    
    
if __name__ == "__main__":
    

    pubsub = r.pubsub()
    pubsub.subscribe("latency")

    for message in pubsub.listen():
        print("Message:", message)
        if message["type"] == "message":
            payload = json.loads(message["data"])
            print("Received:", payload)
            analyze_health_check(payload)
            print("stored:", payload)