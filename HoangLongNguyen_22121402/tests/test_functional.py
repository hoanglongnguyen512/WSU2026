import json
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))
import hello

# ==================== Functional Tests ====================

def test_functional_handler_returns_correct_structure(monkeypatch):
    """Test that handler returns the expected JSON structure"""
    monkeypatch.setattr(hello, "get_websites", lambda: ["https://www.google.com"])
    monkeypatch.setattr(hello, "check_website", lambda url: {
        "url": url, "status": "UP", "availability": 1.0, "latency_ms": 150.5, "status_code": 200
    })
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)

    result = hello.handler({}, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == 200
    assert "timestamp" in body
    assert "results" in body
    assert isinstance(body["results"], list)

def test_functional_multiple_websites(monkeypatch):
    """Test handler with multiple websites"""
    websites = ["https://www.google.com", "https://www.github.com", "https://aws.amazon.com"]
    monkeypatch.setattr(hello, "get_websites", lambda: websites)
    
    def mock_check(url):
        return {"url": url, "status": "UP", "availability": 1.0, "latency_ms": 100, "status_code": 200}
    
    monkeypatch.setattr(hello, "check_website", mock_check)
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)

    result = hello.handler({}, None)
    body = json.loads(result["body"])

    assert len(body["results"]) == 3
    assert all(r["status"] == "UP" for r in body["results"])

def test_functional_mixed_status(monkeypatch):
    """Test handler with both UP and DOWN websites"""
    monkeypatch.setattr(hello, "get_websites", lambda: ["https://up.com", "https://down.com"])
    
    def mock_check(url):
        if "up" in url:
            return {"url": url, "status": "UP", "availability": 1.0, "latency_ms": 80, "status_code": 200}
        return {"url": url, "status": "DOWN", "availability": 0.0, "latency_ms": 5000, "status_code": None}
    
    monkeypatch.setattr(hello, "check_website", mock_check)
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)

    result = hello.handler({}, None)
    body = json.loads(result["body"])

    statuses = [r["status"] for r in body["results"]]
    assert "UP" in statuses
    assert "DOWN" in statuses

def test_functional_metrics_are_published(monkeypatch):
    """Test that metrics are published for each website"""
    call_count = {"count": 0}
    
    def mock_put_metric(*args, **kwargs):
        call_count["count"] += 1
    
    monkeypatch.setattr(hello, "get_websites", lambda: ["https://site1.com", "https://site2.com"])
    monkeypatch.setattr(hello, "check_website", lambda url: {
        "url": url, "status": "UP", "availability": 1.0, "latency_ms": 100, "status_code": 200
    })
    monkeypatch.setattr(hello, "put_metric", mock_put_metric)

    hello.handler({}, None)
    assert call_count["count"] == 4  # 2 websites × 2 metrics (Availability + Latency)

def test_functional_empty_website_list(monkeypatch):
    """Test behavior when no websites are configured"""
    monkeypatch.setattr(hello, "get_websites", lambda: [])
    result = hello.handler({}, None)
    body = json.loads(result["body"])
    
    assert result["statusCode"] == 200
    assert "message" in body
    assert "No website" in body["message"]

def test_functional_latency_recorded(monkeypatch):
    """Test that latency is correctly captured"""
    monkeypatch.setattr(hello, "get_websites", lambda: ["https://example.com"])
    monkeypatch.setattr(hello, "check_website", lambda url: {
        "url": url, "status": "UP", "availability": 1.0, "latency_ms": 245.67, "status_code": 200
    })
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)

    result = hello.handler({}, None)
    body = json.loads(result["body"])
    
    assert body["results"][0]["latency_ms"] == 245.67

def test_functional_availability_zero_when_down(monkeypatch):
    """Test availability is 0.0 when website is down"""
    monkeypatch.setattr(hello, "get_websites", lambda: ["https://down.com"])
    monkeypatch.setattr(hello, "check_website", lambda url: {
        "url": url, "status": "DOWN", "availability": 0.0, "latency_ms": 10000, "status_code": None
    })
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)

    result = hello.handler({}, None)
    body = json.loads(result["body"])
    
    assert body["results"][0]["availability"] == 0.0
    assert body["results"][0]["status"] == "DOWN"

def test_functional_status_code_preserved(monkeypatch):
    """Test that original status code is preserved in result"""
    monkeypatch.setattr(hello, "get_websites", lambda: ["https://example.com"])
    monkeypatch.setattr(hello, "check_website", lambda url: {
        "url": url, "status": "UP", "availability": 1.0, "latency_ms": 90, "status_code": 200
    })
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)

    result = hello.handler({}, None)
    body = json.loads(result["body"])
    
    assert body["results"][0]["status_code"] == 200