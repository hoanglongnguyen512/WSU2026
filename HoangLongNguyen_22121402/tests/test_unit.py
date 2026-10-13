import json
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))
import hello

# ---------- Test check_website ----------
def test_check_website_success():
    result = hello.check_website("https://www.google.com")
    assert result["status"] == "UP"
    assert result["availability"] == 1.0
    assert result["status_code"] == 200
    assert "latency_ms" in result

def test_check_website_returns_url():
    result = hello.check_website("https://www.google.com")
    assert result["url"] == "https://www.google.com"
    
def test_check_website_invalid_url():
    result = hello.check_website("https://invalid-website-12345.com")
    assert result["status"] == "DOWN"
    assert result["availability"] == 0.0
    assert result["status_code"] is None

def test_check_website_timeout():
    with patch("urllib.request.urlopen", side_effect=Exception("Timeout")):
        result = hello.check_website("https://example.com")
        assert result["status"] == "DOWN"
        assert result["availability"] == 0.0

# ---------- Test get_websites ----------
def test_get_websites_empty(monkeypatch):
    mock_table = MagicMock()
    mock_table.scan.return_value = {"Items": []}
    monkeypatch.setattr(hello, "website_table", mock_table)
    assert hello.get_websites() == []

def test_get_websites_with_data(monkeypatch):
    mock_table = MagicMock()
    mock_table.scan.return_value = {
        "Items": [
            {"url": "https://www.google.com"},
            {"url": "https://www.github.com"}
        ]
    }
    monkeypatch.setattr(hello, "website_table", mock_table)
    websites = hello.get_websites()
    assert len(websites) == 2
    assert "https://www.google.com" in websites

# ---------- Test put_metric ----------
def test_put_metric_called(monkeypatch):
    mock_cw = MagicMock()
    monkeypatch.setattr(hello, "cloudwatch", mock_cw)
    hello.put_metric("Latency", 123.45, "https://example.com", "Milliseconds")
    mock_cw.put_metric_data.assert_called_once()

# ---------- Test handler ----------
def test_handler_no_websites(monkeypatch):
    monkeypatch.setattr(hello, "get_websites", lambda: [])
    result = hello.handler({}, None)
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert "No website to monitor" in body["message"]

def test_handler_with_websites(monkeypatch):
    monkeypatch.setattr(hello, "get_websites", lambda: ["https://www.google.com"])
    monkeypatch.setattr(hello, "check_website", lambda url: {
        "url": url, "status": "UP", "availability": 1.0, "latency_ms": 100, "status_code": 200
    })
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)
    
    result = hello.handler({}, None)
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert len(body["results"]) == 1

def test_handler_returns_timestamp(monkeypatch):
    monkeypatch.setattr(hello, "get_websites", lambda: ["https://www.google.com"])
    monkeypatch.setattr(hello, "check_website", lambda url: {
        "url": url, "status": "UP", "availability": 1.0, "latency_ms": 100, "status_code": 200
    })
    monkeypatch.setattr(hello, "put_metric", lambda *args, **kwargs: None)
    
    result = hello.handler({}, None)
    body = json.loads(result["body"])
    assert "timestamp" in body