from aws_cdk import core

from .aws_cdk_pipeline_test_stack import AwsCdkPipelineTestStack

class WebServiceStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    service = AwsCdkPipelineTestStack(self, 'WebService')

    self.url_output = service.url_output