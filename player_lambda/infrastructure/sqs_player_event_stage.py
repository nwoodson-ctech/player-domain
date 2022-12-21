from aws_cdk import (
    Stage
)
from constructs import Construct

from player_lambda.infrastructure.sqs_player_event_stack import SQSPlayerEventStack


class SQSPlayerEventStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        SQSPlayerEventStack(self, 'SQSPlayerEventStack')
