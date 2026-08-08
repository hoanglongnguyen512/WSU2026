import json
import time
import urllib.request
import urllib.error

def handler(event, context):
    url = "https://www.westernsydney.edu.au/"
    
    start_time = time.time()
    
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            response_time = round((time.time() - start_time) * 1000, 2)  # milliseconds
            
            result = {
                "url": url,
                "status_code": status_code,
                "response_time_ms": response_time,
                "status": "UP" if status_code == 200 else "DOWN",
                "message": "Website is reachable"
            }
    except Exception as e:
        response_time = round((time.time() - start_time) * 1000, 2)
        result = {
            "url": url,
            "status_code": None,
            "response_time_ms": response_time,
            "status": "DOWN",
            "message": str(e)
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps(result, indent=2)
    }
