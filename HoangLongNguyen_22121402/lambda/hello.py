import json
import time
import urllib.request
import urllib.error
import boto3
from datetime import datetime

cloudwatch = boto3.client('cloudwatch')

# List of website have to be monitored
WEBSITES = [
    "https://www.westernsydney.edu.au/",
    "https://www.google.com/",
    "https://www.github.com/",
    "https://aws.amazon.com/"
]

def put_metric (metric_name, value, website, unit= 'None'):
    cloudwatch.put_metric_data(
        Namespace='WebHealth',
        MetricData= [
            {
                'MetricName': metric_name,
                'Dimensions': [
                    {'Name' : 'Website', 'Value': website}
                ],
                'Timestamp' : datetime.utcnow(),
                'Value': value,
                'Unit': unit
            }
        ]
    )

def check_website(url):
    start = time.time()
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            latency = round((time.time() - start) * 1000, 2)
            availability = 1.0 if status_code == 200 else 0.0
            return {
                "url": url,
                "status_code": status_code,
                "latency_ms": latency,
                "availability": availability,
                "status": "UP" if availability == 1.0 else "DOWN"
            }
    except Exception as e:
        latency = round((time.time() - start) * 1000, 2)
        return {
            "url": url,
            "status_code": None,
            "latency_ms": latency,
            "availability": 0.0,
            "status": "DOWN",
            "error": str(e)
        }

def handler(event, context):
    results = []
    
    for url in WEBSITES:
        result = check_website(url)
        results.append(result)
        
        # Apply metrics on CloudWatch
        put_metric('Availability', result['availability'], url, unit='None')
        put_metric('Latency', result['latency_ms'], url, unit='Milliseconds')
        
        print(f"Checked {url}: {result['status']} | Latency: {result['latency_ms']}ms")
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "results": results
        }, indent=2)
    }