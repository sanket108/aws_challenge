import boto3
import os
import json
import uuid

dynamodb = boto3.resource("dynamodb")
ec2 = boto3.client("ec2")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    try:
        # Create VPC
        vpc_response = ec2.create_vpc(CidrBlock="10.0.0.0/16")
        vpc_id = vpc_response['Vpc']['VpcId']

        # Create subnets
        subnets = []
        for i in range(2):
            subnet = ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=f"10.0.{i}.0/24"
            )
            subnets.append(subnet['Subnet']['SubnetId'])
        
        # Store in DynamoDB
        table.put_item(
            Item={
                "vpc_id": vpc_id,
                "subnets": subnets
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "VPC and Subnets created successfully.",
                "vpc_id": vpc_id,
                "subnets": subnets
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }