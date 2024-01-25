from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigateway as _apigateway,
    Duration
)
from constructs import Construct


class BedrockAgentCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 需要先通过readme中写的内容创建boto3 layer，然后将ARN放到下面
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
        bedrock_api = _apigateway.RestApi(
            self, "bedrock-api",
            rest_api_name="BedrockApi",
            description="Bedrock API Gateway",
            deploy=True,
            deploy_options=_apigateway.StageOptions(stage_name='prod')
        )

        request_validator = _apigateway.RequestValidator(self,
                                                         id="bedrock-request-validator",
                                                         rest_api=bedrock_api,
                                                         request_validator_name="RequestBodyValidator",
                                                         validate_request_body=True)

        from aws_cdk.aws_apigateway import JsonSchemaType
        request_model = _apigateway.Model(self,
                                          id="modelValidator",
                                          model_name="modelValidator",
                                          rest_api=bedrock_api,
                                          content_type="application/json",
                                          description="To validate the request body",
                                          schema={
                                              "type": JsonSchemaType.OBJECT,
                                              "properties": {
                                                  "sessionId": {"type": JsonSchemaType.STRING, "minLength": 1},
                                                  "inputText": {"type": JsonSchemaType.STRING, "minLength": 1},
                                                  "enableTrace": {"type": JsonSchemaType.BOOLEAN},
                                                  "endSession": {"type": JsonSchemaType.BOOLEAN}
                                              },
                                              "required": ["sessionId", "inputText", "enableTrace", "endSession"]
                                          })

        chat_path = bedrock_api.root.add_resource(
            path_part='chat', default_method_options=_apigateway.MethodOptions(api_key_required=True)
        )

        integration = _apigateway.LambdaIntegration(function)
        chat_path.add_method("POST", integration,
                             request_parameters={"method.request.header.Content-Type": True},
                             request_validator=request_validator,
                             request_models={"application/json": request_model})

        usage_plan = bedrock_api.add_usage_plan("BedrockAPIUsagePlan", name="myPlan")
        usage_plan.add_api_stage(stage=bedrock_api.deployment_stage)
        api_key = bedrock_api.add_api_key('MyBedrockAPIKey')
        usage_plan.add_api_key(api_key)
