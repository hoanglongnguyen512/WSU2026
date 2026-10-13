import json
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))
import hello

# ==================== Integration Tests ====================

def test_integration_full_flow_with_mock_dynamodb(monkeypatch):
    """
    Integration test: Simulate reading websites from DynamoDB
    and checking them through the full handler flow.
    """
    # Mock DynamoDB scan to return 2 websites
    mock_table = MagicMock()
    mock_table.scan.return_value = {
        "Items": [
            {"url": "https://www.google.com"},
            {"url": "https://www.github.com"}
        ]
    }
    monkeypatch.setattr(hello, "website_table", mock_table)

    # Mock check_website to return realistic results
    def mock_check(url):
        if "google" in url:
            return {
                "url": url,
                "status_code": 200,
                "latency_ms": 120.5,
                "availability": 1.0,
                "status": "UP"
            }
        return {
            "url": url,
            "status_code": 200,
            "latency_ms": 85.3,
            "availability": 1.0,
            "status": "UP"
        }

    monkeypatch.setattr(hello, "check_website", mock_check)
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)

    # Run the full handler
    result = hello.handler({}, None)
    body = json.loads(result["body"])

    # Assertions
    assert result["statusCode"] == 200
    assert len(body["results"]) == 2
    assert body["results"][0]["status"] == "UP"
    assert body["results"][1]["status"] == "UP"
    assert "timestamp" in body

def test_integration_error_handling_when_website_fails(monkeypatch):
    """
    Integration test: Test the full flow when one website fails to respond.
    """
    mock_table = MagicMock()
    mock_table.scan.return_value = {
        "Items": [
            {"url": "https://www.google.com"},
            {"url": "https://invalid-site-xyz.com"}
        ]
    }
    monkeypatch.setattr(hello, "website_table", mock_table)

    def mock_check(url):
        if "google" in url:
            return {
                "url": url,
                "status_code": 200,
                "latency_ms": 95.0,
                "availability": 1.0,
                "status": "UP"
            }
        # Simulate failure
        return {
            "url": url,
            "status_code": None,
            "latency_ms": 10000,
            "availability": 0.0,
            "status": "DOWN",
            "error": "Connection failed"
        }

    monkeypatch.setattr(hello, "check_website", mock_check)
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)

    result = hello.handler({}, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == 200
    assert len(body["results"]) == 2

    # One UP, one DOWN
    statuses = [r["status"] for r in body["results"]]
    assert "UP" in statuses
    assert "DOWN" in statuses