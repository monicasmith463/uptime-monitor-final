from src.database import SessionLocal
from src.models import HealthCheck
from src.services.analyzer import analyze_health_check


def test_analyze_health_check():
    payload = {"site": "https://example.com",
        "response_time": 0.5,
        "status_code": 200,
        "error": None}
    analyze_health_check(payload)
    db = SessionLocal()
    try:
        analyzed_health_check = db.query(HealthCheck).first()

        assert analyzed_health_check is not None
        assert analyzed_health_check.response_time > 0
        assert analyzed_health_check.status_code == 200
        assert analyzed_health_check.error is None

    finally:
        db.close()