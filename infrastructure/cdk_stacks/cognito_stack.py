from aws_cdk import (
    Stack,
    aws_cognito as cognito,
)
from constructs import Construct

class CognitoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_config: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Cognito User Pool
        self.user_pool = cognito.UserPool(self, "UserPool",
        self_sign_up_enabled=True,
        sign_in_aliases=cognito.SignInAliases(email=True))
        
        self.user_pool_client = cognito.UserPoolClient(
            self, "UserPoolClient",
            user_pool=self.user_pool,
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            )
        )