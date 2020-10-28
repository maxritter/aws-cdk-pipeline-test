#!/usr/bin/env python3

from aws_cdk import core

from aws_cdk_pipeline_test.pipelines_stack import PipelineStack

app = core.App()
PipelineStack(app, 'aws-cdk-pipeline-test', env=core.Environment(account="356419192138", region="eu-central-1"))
app.synth()
