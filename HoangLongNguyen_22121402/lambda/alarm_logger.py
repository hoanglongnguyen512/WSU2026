import json
import os
import uuid
from datetime import datetime
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["ALARM_TABLE_NAME"])

def handler(event, context):
    for record in event.get("Records", []):
        message = record.get("Sns", {}).get("Message", "{}")
        try:
            payload = json.loads(message)
        except Exception:
            payload = {"raw": message}

        item = {
            "alarm_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "alarm_name": payload.get("AlarmName", "Unknown"),
            "new_state": payload.get("NewStateValue", "Unknown"),
            "reason": payload.get("NewStateReason", ""),
            "message": message
        }
        table.put_item(Item=item)

    return {"statusCode": 200}