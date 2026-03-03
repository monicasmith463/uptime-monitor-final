from unittest.mock import MagicMock, patch

from src.services.analyzer import analyze_health_check


def test_should_save_successful_health_check_to_db():
    fake_site = MagicMock()
    fake_site.id = 1
    fake_session = MagicMock()
    query_mock = fake_session.query.return_value
    filter_mock = query_mock.filter.return_value
    filter_mock.first.return_value = fake_site

    payload = {"site": "https://test.com", "response_time": 0.12235, "status_code": 200, "error": None}
    with patch("src.services.analyzer.SessionLocal", return_value=fake_session):
        fake_session.return_value = fake_session
        analyze_health_check(payload)

    fake_session.add.assert_called_once()
    fake_session.commit.assert_called_once()

