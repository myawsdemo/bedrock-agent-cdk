import json
import boto3

print("boto3 version:" + boto3.__version__)

agent = boto3.client('bedrock-agent-runtime')


def lambda_handler(event, context):
    body = json.loads(event['body'])

    print(body)

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
        agentAliasId='BL23NH1CZC',
        sessionId=body['sessionId'],
        endSession=body['endSession'],
        enableTrace=body['enableTrace'],
        inputText=body['inputText']
    )
    event_stream = response['completion']
    print(response)
    msg = ''
    for event in event_stream:
        if 'chunk' in event:
            msg += event['chunk']['bytes'].decode("utf-8")
    print(msg)

    # TODO implement
    return {
        'statusCode': 200,
        'body': msg
    }