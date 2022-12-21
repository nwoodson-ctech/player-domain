from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as python,
    aws_events as events,
    aws_kinesis as kinesis
)
from constructs import Construct


class StreamPlayerEventStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stream_player_event_handler = python.PythonFunction(self, "StreamPlayerEventHandler",
                                                            entry="player_lambda/runtime",  # required
                                                            runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                                            index="stream_player_event_handler.py",
                                                            # optional, defaults to 'index.py'
                                                            handler="handler",
                                                            memory_size=256,
                                                            function_name="StreamPlayerEventHandler"
                                                            )

        event_bride_service_principal = iam.ServicePrincipal("events.amazonaws.com")
        stream_player_event_handler.grant_invoke(event_bride_service_principal)

        player_data_event_bus = events.EventBus.from_event_bus_name(
            self, "PlayerDataEventBus", "PlayerDataEventBus")

        player_data_event_bus.grant_put_events_to(stream_player_event_handler)

        player_domain_stream = kinesis.Stream.from_stream_arn(
            self,
            "PlayerStream",
            "arn:aws:kinesis:us-east-1:499104388492:stream/player-domain-stream")

        player_domain_stream.grant_write(stream_player_event_handler)
