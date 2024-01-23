import json
import boto3

print("boto3 version:" + boto3.__version__)

agent = boto3.client('bedrock-agent-runtime')
accept = 'application/json'
contentType = 'application/json'


def lambda_handler(event, context):
    response = agent.invoke_agent(
        sessionState={
            'sessionAttributes': {
                'string': 'string'
            },
            'promptSessionAttributes': {
                'string': 'string'
            }
        },
        agentId='DTSC5QHP98',
        agentAliasId='UK0FRQTLMZ',
        sessionId='session998',
        endSession=True,
        enableTrace=False,
        inputText='谢谢'
    )
    event_stream = response['completion']
    for event in event_stream:
        if 'chunk' in event:
            data = event['chunk']['bytes'].decode("utf-8")
            print(data)

    # TODO implement
    return {
        'statusCode': 200,
        'body': response
    }