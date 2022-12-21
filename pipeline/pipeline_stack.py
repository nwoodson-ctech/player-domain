from constructs import Construct
from aws_cdk import (
    Stack,
    pipelines as pipelines,
    SecretValue
)

from player_lambda.infrastructure.add_player_event_stage import AddPlayerEventStage
from event_bridge.infrastructure.player_event_bridge_stage import PlayerEventBridgeStage
from player_lambda.infrastructure.stream_player_event_stage import StreamPlayerEventStage
from player_lambda.infrastructure.sqs_player_event_stage import SQSPlayerEventStage


class PipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        code_pipeline = pipelines.CodePipeline(
            self,
            'Player-Pipeline',
            docker_enabled_for_synth=True,
            synth=pipelines.ShellStep('Synth',
                                      input=pipelines.CodePipelineSource.git_hub(
                                          'nwoodson-ctech/player-domain',
                                          'main',
                                          authentication=SecretValue.secrets_manager(
                                              'exploration-token')
                                      ),
                                      env={'privileged': 'True'},
                                      commands=[
                                          "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                                          # Instructs Codebuild to install required packages
                                          "pip3 install -r requirements.txt",
                                          "cdk synth"
                                      ]
                                      )
        )


        deploy_add_player_event = AddPlayerEventStage(
            self, "DeployAddPlayerEvent")
        code_pipeline.add_stage(
            deploy_add_player_event)

        deploy_player_event_bridge = PlayerEventBridgeStage(
            self, "DeployPlayerEventBridge")
        code_pipeline.add_stage(
            deploy_player_event_bridge)

        deploy_stream_player_event = StreamPlayerEventStage(
            self, "DeployStreamPlayerEventHandler"
        )
        code_pipeline.add_stage(deploy_stream_player_event)

        deploy_sqs_player_event = SQSPlayerEventStage(
            self, "DeploySQSPlayerEventHandler"
        )
        code_pipeline.add_stage(deploy_sqs_player_event)
