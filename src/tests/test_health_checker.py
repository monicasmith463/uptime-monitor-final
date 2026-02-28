from unittest.mock import MagicMock, patch

from src.services.health_checker import health_check

    
def test_health_check_success():
    fake_response = MagicMock()
    fake_response.status_code = 200

    with patch("src.services.health_checker.requests.get", return_value=fake_response):
        result = health_check("https://example.com")
        assert result["site"] == "https://example.com"
        assert result["response_time"] > 0
        assert result["status_code"] == 200
        assert result["error"] is None



def test_health_check_fail():
    fake_response = MagicMock()
    fake_response.status_code = 500

    with patch("src.services.health_checker.requests.get", return_value=fake_response):
        result = health_check("https://example.com")
        assert result["site"] == "https://example.com"
        assert result["status_code"] == 500
