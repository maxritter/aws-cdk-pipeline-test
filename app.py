#!/usr/bin/env python3

from aws_cdk import core

from aws_cdk_pipeline_test.aws_cdk_pipeline_test_stack import AwsCdkPipelineTestStack
from aws_cdk_pipeline_test.pipelines_stack import PipelineStack

app = core.App()
AwsCdkPipelineTestStack(app, "aws-cdk-test")
PipelineStack(app, 'aws-cdk-pipeline-test', env=core.Environment(account="298767276755", region="eu-central-1"))
app.synth()
