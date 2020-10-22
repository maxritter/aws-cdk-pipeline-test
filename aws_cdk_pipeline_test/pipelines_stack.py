from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from .webservice_stage import WebServiceStage

APP_ACCOUNT_DEV = '298767276755'
APP_ACCOUNT_PROD = '614027750584'

class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'Pipeline',
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name='WebinarPipeline',

            source_action=cpactions.GitHubSourceAction(
                action_name='GitHub',
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager('github-token'),
                owner='maxritter',
                repo='aws-cdk-pipeline-test',
                trigger=cpactions.GitHubTrigger.POLL),

            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                build_command='pytest unittests',
                synth_command='cdk synth'))

        pre_prod_app = WebServiceStage(self, 'Pre-Prod', env={
            'account': APP_ACCOUNT_DEV,
            'region': 'eu-central-1',
        })
        pre_prod_stage = pipeline.add_application_stage(pre_prod_app)
        pre_prod_stage.add_manual_approval_action(
            action_name='PromoteToProd'
        )

        prod_app = WebServiceStage(self, 'Prod', env={
            'account': APP_ACCOUNT_PROD,
            'region': 'eu-central-1',
        })
        prod_stage = pipeline.add_application_stage(prod_app)