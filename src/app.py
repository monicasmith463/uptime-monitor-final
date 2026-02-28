from datetime import datetime, timedelta
import time

from flask import Flask, g, render_template, request, jsonify, redirect, url_for
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from src.config import r
from src.database import SessionLocal
from src.models import HealthCheck, Site
from prometheus_client import Gauge, make_wsgi_app, Counter, Histogram

from werkzeug.middleware.dispatcher import DispatcherMiddleware


app = Flask(__name__)

# tutorial resource: https://medium.com/@letathenasleep/exposing-python-metrics-with-prometheus-c5c837c21e4d
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Gauge - tracks current values
dependency_up = Gauge(
    'dependency_up',
    'Number of dependency up.',
    ['service']
)


requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_latency = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if request.path == "/metrics":
        return response
        
    requests_total.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    if g.start_time:
        latency = time.time() - g.start_time
        request_latency.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown'
        ).observe(latency)

        

   

    return response

def get_all_sites():
    db = SessionLocal()
    try:
        sites = db.query(Site).all()
        return sites
        
    except Exception as e:
        print("get all sites failed")
    finally:
        db.close()

def get_recent_health_checks(limit=50):
    db = SessionLocal()
    try:

        health_checks = (
            db.query(HealthCheck)
            .options(joinedload(HealthCheck.site))
            .order_by(HealthCheck.created_at.desc())
            .limit(limit)
            .all()
        )
        return health_checks
        
    except Exception as e:
        print("get_recent_health_checks failed")
    finally:
        db.close()


def db_add_site(url):
    url = url.strip()
    if url.endswith("/") and url not in ("http://", "https://"):
        url = url[:-1]
    db = SessionLocal()
    try:
        db.add(Site(url=url))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("That site is already in the list.")
    except Exception as e:
        db.rollback()
        print("add_site failed for URL:", url, e)
        raise
    finally:
        db.close()

@app.route("/", methods=["POST"])
def add_site():
    input_text = request.form.get("site", "").strip()
    if not input_text:
        return "No site provided", 400
    try:
        db_add_site(input_text)
        return redirect(url_for("main"))
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return "Error adding site: " + str(e), 500

@app.route("/")
def main():   
    checks = get_recent_health_checks()
    sites = get_all_sites()
    return render_template("index.html", sites=sites, checks=checks)

# health check logic is below/
# reference: https://www.index.dev/blog/how-to-implement-health-check-in-python


def check_database() -> bool:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
    finally:
        db.close()


def check_redis() -> bool:
    try:
        return r.ping()
    except Exception:
        return False


@app.route('/health', methods=['GET'])
def health():
    db_healthy = check_database()
    redis_healthy = check_redis()

    # monitoring.
    dependency_up.labels(service="db").set(1 if db_healthy else 0)
    dependency_up.labels(service="redis").set(1 if redis_healthy else 0)
    status = None
    payload = {}

    if db_healthy and redis_healthy:
        payload = {
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
        }
        status = 200
    else:
        payload = {
            "status": "unhealthy",
            "database": "connected" if db_healthy else "disconnected",
            "redis": "connected" if redis_healthy else "disconnected",
        }
        status = 503

    return jsonify(payload), status

