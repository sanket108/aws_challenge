from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

class DynamoDBStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_config: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB table
        self.table = dynamodb.Table(
            self, "VpcMetadataTable",
            partition_key=dynamodb.Attribute(name="vpc_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )