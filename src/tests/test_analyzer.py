from unittest.mock import MagicMock, patch

from src.services.analyzer import analyze_health_check


def test_analyze_health_check_success():
    fake_site = MagicMock()
    fake_site.id = 1
    fake_session = MagicMock()
    fake_session.query.return_value.filter.return_value.first.return_value = fake_site

    payload = {"site": "https://example.com", "response_time": 0.5, "status_code": 200, "error": None}
    with patch("src.services.analyzer.SessionLocal", return_value=fake_session):
        analyze_health_check(payload)

    fake_session.add.assert_called_once()
    fake_session.commit.assert_called_once()
    fake_session.close.assert_called_once()

