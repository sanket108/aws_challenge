from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
)
from constructs import Construct

class ApiGatewayStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_config: dict, table, user_pool, user_pool_client, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda Role
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            ]
        )

        # Lambda: Create VPC
        create_vpc_lambda = _lambda.Function(
            self, "CreateVpcFunction",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="create_vpc_lambda.handler",
            code=_lambda.Code.from_asset('../lambda/python'),
            role=lambda_role,
            environment={"TABLE_NAME": table.table_name}
        )

        # Lambda: Get VPC
        get_vpc_lambda = _lambda.Function(
            self, "GetVpcFunction",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="get_vpc_lambda.handler",
            code=_lambda.Code.from_asset('../lambda/python'),
            role=lambda_role,
            environment={"TABLE_NAME": table.table_name}
        )

        # API Gateway
        api = apigateway.RestApi(self, "VpcApi", rest_api_name="VPC Service")

        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self, "VpcAuthorizer",
            cognito_user_pools=[user_pool]
        )

        vpc_resource = api.root.add_resource("vpc")

        vpc_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(create_vpc_lambda),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        vpc_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_vpc_lambda),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )