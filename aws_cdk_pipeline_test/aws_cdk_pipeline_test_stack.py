from aws_cdk.core import Stack, StackProps, Construct, SecretValue
from aws_cdk.pipelines import CdkPipeline, SimpleSynthAction

import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as codepipeline_actions

class AwsCdkPipelineTestStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Output artifact
        source_artifact = codepipeline.Artifact()
        # Artifact to hold the cloudAssemblyArtifact for the synth action (the template)
        cloud_assembly_artifact = codepipeline.Artifact()

        # Source
        source_action=codepipeline_actions.GitHubSourceAction(
            action_name="GitHub",
            output=source_artifact,
            oauth_token=SecretValue.secrets_manager("github-token"),
            trigger=codepipeline_actions.GitHubTrigger.POLL,
            # Replace these with your actual GitHub project info
            owner="maxritter",
            repo="aws-cdk-pipeline-test")


        # Build (On synth)
        synth_action = SimpleSynthAction(
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            synth_command="cdk synth",
        )

        # Define an AWS CodePipeline-based Pipeline to deploy CDK applications
        pipeline = CdkPipeline(
            self,
            "Pipeline",
            pipeline_name="MyAppPipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_action=source_action,
            synth_action=synth_action,
        )
        
