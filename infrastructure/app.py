#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk_stacks.dynamodb_stack import DynamoDBStack
from cdk_stacks.cognito_stack import CognitoStack
from cdk_stacks.api_gateway_stack import ApiGatewayStack

# Pull the AWS account # and region from env variables. See https://docs.aws.amazon.com/cdk/v2/guide/environments.html
# for the source of this approach.
aws_account = os.environ.get('CDK_DEPLOY_ACCOUNT', os.environ['CDK_DEFAULT_ACCOUNT'])
aws_region = os.environ.get('CDK_DEPLOY_REGION', os.environ['CDK_DEFAULT_REGION'])
aws_env = cdk.Environment(account=aws_account, region=aws_region)


app = cdk.App()
env_name = app.node.try_get_context('env')
env_config = app.node.try_get_context('environment')[env_name]
env_config['suffix'] = app.node.try_get_context('suffix')

dynamodb_stack = DynamoDBStack(app, "DynamoDBStack", env_config, tags=env_config['tags'], env=aws_env, description='Dynamo db table for project')

cognito_stack = CognitoStack(app, "CognitoStack", env_config, tags=env_config['tags'], env=aws_env, description='Cognito user pool and client for project')

ApiGatewayStack(app, "ApiGatewayStack", env_config, tags=env_config['tags'], env=aws_env, 
    table = dynamodb_stack.table, 
    user_pool= cognito_stack.user_pool,
    user_pool_client= cognito_stack.user_pool_client,
    description='API gateway for project')

app.synth()