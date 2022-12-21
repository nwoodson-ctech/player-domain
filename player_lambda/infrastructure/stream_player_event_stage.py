from aws_cdk import (
    Stage
)
from constructs import Construct

from player_lambda.infrastructure.stream_player_event_stack import StreamPlayerEventStack


class StreamPlayerEventStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        StreamPlayerEventStack(self, 'StreamPlayerEventStack')
