import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

client = boto3.client('sqs')

logger = Logger(service="SQSPlayerEventHandler")


@event_source(data_class=SQSEvent)
@logger.inject_lambda_context
def handler(event: SQSEvent, context: LambdaContext) -> str:
    # Multiple records can be delivered in a single event
    for record in event.records:
        data = record.body

        logger.info(data)

        message_sent = client.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/499104388492/player-sqs-stack-1029',
            MessageBody=data
        )

    result = {
        "statusCode": 200,
        "headers": {
            "content-type": "application/json"
        },
        "body": message_sent
    }

    logger.info(result)

    return result
