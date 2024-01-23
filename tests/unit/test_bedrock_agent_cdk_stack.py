import aws_cdk as core
import aws_cdk.assertions as assertions

from bedrock_agent_cdk.bedrock_agent_cdk_stack import BedrockAgentCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in bedrock_agent_cdk/bedrock_agent_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BedrockAgentCdkStack(app, "bedrock-agent-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
