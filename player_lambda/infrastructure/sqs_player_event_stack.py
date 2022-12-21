from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as python,
    aws_sqs as sqs,
    aws_lambda as lambda_
)
from constructs import Construct


class SQSPlayerEventStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sqs_player_event_handler = python.PythonFunction(self, "SQSPlayerEventHandler",
                                                         entry="player_lambda/runtime",  # required
                                                         runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                                         index="sqs_player_event_handler.py",
                                                         # optional, defaults to 'index.py'
                                                         handler="handler",
                                                         memory_size=256,
                                                         function_name="SQSPlayerEventHandler"
                                                         )

        event_bride_service_principal = iam.ServicePrincipal("events.amazonaws.com")
        sqs_player_event_handler.grant_invoke(event_bride_service_principal)

        player_sqs = sqs.Queue.from_queue_arn(
            self,
            "PlayerSQS",
            "arn:aws:sqs:us-east-1:499104388492:player-sqs-stack-1029")

        player_sqs.grant_consume_messages(sqs_player_event_handler)

        lambda_.EventSourceMapping(
            self,
            "PlayerSQSEventSourceMapping",
            target=sqs_player_event_handler,
            event_source_arn="arn:aws:sqs:us-east-1:499104388492:player-sqs-stack-1029")
