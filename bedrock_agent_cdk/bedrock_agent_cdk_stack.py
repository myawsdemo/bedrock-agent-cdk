from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigateway as api_gateway,
    Duration
)
from constructs import Construct


class BedrockAgentCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        layer_arn = "arn:aws:lambda:us-east-1:715371302281:layer:boto3-mylayer:1"

        # 引用已有的 Lambda Layer
        boto3_layer = _lambda.LayerVersion.from_layer_version_arn(
            self, "MyLayer",
            layer_arn,
        )

        # 创建 IAM 角色并为 Lambda 函数授权
        lambda_role = iam.Role(
            self, "MyLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_managed_policy_arn(self, 'bedrock-full-access',
                                                                        'arn:aws:iam::aws:policy/AmazonBedrockFullAccess'),
                              iam.ManagedPolicy.from_managed_policy_arn(self, 'lambda-basic-access',
                                                                        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')
                              ],  # 将 AWS 托管策略添加到角色中
        )

        # The code that defines your stack goes here
        function = _lambda.Function(self, "Bedrock_Agent_Call",
                                    runtime=_lambda.Runtime.PYTHON_3_12,
                                    handler="bedrock_agent_call.lambda_handler",
                                    code=_lambda.Code.from_asset("bedrock_agent_cdk/lambda"),
                                    layers=[boto3_layer],
                                    role=lambda_role,
                                    function_name='Bedrock_Agent_Call',
                                    timeout=Duration.seconds(120)
                                    )
        gateway = api_gateway.RestApi(
            self, "bedrock-api",
            rest_api_name="BedrockApi",
            description="Bedrock API Gateway",
        )

        apiKey = api_gateway.ApiKey(
            self, 'MyBedrockAPIKey', api_key_name='bedrock-api-key', enabled=True, description='api gateway key'
        )

        chat_path = gateway.root.add_resource(
            path_part='chat', default_method_options=api_gateway.MethodOptions(api_key_required=True)
        )

        integration = api_gateway.LambdaIntegration(function)
        chat_path.add_method("POST", integration, request_parameters={"method.request.header.Content-Type": True})
