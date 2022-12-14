import base64
import json

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, EventBridgeEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

client = boto3.client('kinesis')

logger = Logger(service="StreamPlayerEventHandler")


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context
def handler(event: EventBridgeEvent, context: LambdaContext) -> str:
    event_bus_detail_data = str(event.detail)
    logger.info(event_bus_detail_data)

    event_bus_detail_data_encoded = base64.b64encode(event_bus_detail_data.encode('ascii'))
    logger.info(event_bus_detail_data_encoded)

    client.put_record(
        StreamName="player-domain-stream",
        Data=event_bus_detail_data_encoded,
        PartitionKey="SavePlayer"
    )

    result = {
        "statusCode": 200,
        "headers": {
            "content-type": "application/json"
        },
        "body": event_bus_detail_data
    }

    logger.info(result)

    return result
