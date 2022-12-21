from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    aws_events as events,
    aws_events_targets as target,
    aws_iam as iam,
    aws_lambda_python_alpha as python
)


class PlayerEventBridgeStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ### Create Player Event Bus ###
        player_event_bus = events.EventBus(self,
                                           id='player-event-bus',
                                           event_bus_name='PlayerEventBus'
                                           )

        ### Create Player Event Bus Archive ###
        player_event_bus.archive('PlayerEventBusArchive',
                                 archive_name='PlayerEventBusArchive',
                                 description='PlayerEventBus Archive',
                                 event_pattern=events.EventPattern(
                                     account=[Stack.of(self).account]
                                 ),
                                 retention=Duration.days(1)
                                 )

        add_player_rule = events.Rule(self, "add-player-rule",
                                      event_bus=player_event_bus,
                                      event_pattern=events.EventPattern(
                                            detail_type=["player"],
                                            detail={
                                                "eventName": ["AddPlayer"]
                                            },
                                      )
                                      )

        add_player_lambda = python.PythonFunction.from_function_name(
            self, "AddPlayerEventHandler", "AddPlayerEventHandler")

        add_player_rule.add_target(
            target.LambdaFunction(
                add_player_lambda
            ))

        save_player_rule = events.Rule(self, "save-player-rule",
                                      event_bus=player_event_bus,
                                      event_pattern=events.EventPattern(
                                            detail_type=["player"],
                                            detail={
                                                "eventName": ["SavePlayer"]
                                            },
                                      )
                                      )

        stream_player_lambda = python.PythonFunction.from_function_name(
            self, "StreamPlayerEventHandler", "StreamPlayerEventHandler")

        save_player_rule.add_target(
            target.LambdaFunction(
                stream_player_lambda
            ))