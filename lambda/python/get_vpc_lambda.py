import boto3
import os
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    try:
        scan_result = table.scan()
        return {
            "statusCode": 200,
            "body": json.dumps(scan_result.get("Items", []))
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }