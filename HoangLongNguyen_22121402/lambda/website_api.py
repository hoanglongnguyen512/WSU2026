import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["WEBSITE_TABLE_NAME"])

def handler(event, context):
    method = event.get("httpMethod", "")
    path = event.get("path", "")

    if method == "GET" and path == "/websites":
        response = table.scan()
        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", []))
        }

    if method == "POST" and path == "/websites":
        body = json.loads(event.get("body", "{}"))
        url = body.get("url")
        if not url:
            return {"statusCode": 400, "body": json.dumps({"error": "url is required"})}
        table.put_item(Item={"url": url})
        return {"statusCode": 201, "body": json.dumps({"message": "Website added", "url": url})}

    if method == "DELETE" and path.startswith("/websites/"):
        url = path.split("/websites/")[-1]
        table.delete_item(Key={"url": url})
        return {"statusCode": 200, "body": json.dumps({"message": "Website deleted"})}

    return {"statusCode": 404, "body": json.dumps({"error": "Not found"})}